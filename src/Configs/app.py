from datetime import timedelta
import json
from urllib.parse import urlparse

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notehub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

db = SQLAlchemy(app)
jwt = JWTManager(app)

CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=False
)


# User table for storing registered accounts.
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


# Note table for storing uploaded notes
class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(100))
    fileLink = db.Column(db.String(255))
    links = db.Column(db.Text, default="[]")
    editable_by_others = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref="notes")


# NoteVersion table for saving old note versions.
class NoteVersion(db.Model):
    __tablename__ = "note_versions"

    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(100))
    fileLink = db.Column(db.String(255))
    links = db.Column(db.Text, default="[]")
    editable_by_others = db.Column(db.Boolean, default=False)
    edited_at = db.Column(db.DateTime, server_default=db.func.now())
    edited_by = db.Column(db.String(100))

    note = db.relationship("Note", backref="versions")


# Gets the logged-in user's ID from the JWT token.
def get_current_user_id():
    identity = get_jwt_identity()

    if identity is None:
        return None

    try:
        return int(identity)
    except (TypeError, ValueError):
        return None


# Checks if the user can edit a note.
def can_edit_note(note, user_id):
    if not note or user_id is None:
        return False

    try:
        return int(note.user_id) == int(user_id) or bool(note.editable_by_others)
    except (TypeError, ValueError):
        return False


# Checks if a given URL uses http or https.
def is_valid_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ("http", "https") and bool(parsed_url.netloc)


# Cleans and validates attached links before saving.
def normalize_links(raw_links):
    if raw_links in (None, ""):
        return []

    if not isinstance(raw_links, list):
        raise ValueError("Links must be provided as a list.")

    normalized_links = []

    for raw_link in raw_links:
        if not isinstance(raw_link, str):
            raise ValueError("Each link must be a URL string.")

        link = raw_link.strip()

        if not link:
            raise ValueError("Empty links cannot be saved.")

        if not is_valid_url(link):
            raise ValueError("Please provide valid http or https links.")

        if link not in normalized_links:
            normalized_links.append(link)

    return normalized_links


# Converts the links list into JSON text for SQLite.
def serialize_links(raw_links):
    return json.dumps(normalize_links(raw_links))


# Converts saved JSON link text back into a Python list.
def deserialize_links(links_json):
    if not links_json:
        return []

    try:
        links = json.loads(links_json)
    except (TypeError, json.JSONDecodeError):
        return []

    return links if isinstance(links, list) else []


# Converts a Note object into JSON-ready data for the frontend.
def note_to_dict(note, current_user_id=None):
    username = note.user.name if note.user else "Unknown"
    date_str = note.date_created.strftime("%b %d, %Y") if note.date_created else ""

    return {
        "id": note.id,
        "title": note.title,
        "description": note.description,
        "subject": note.subject,
        "fileLink": note.fileLink,
        "links": deserialize_links(note.links),
        "editable_by_others": bool(note.editable_by_others),
        "can_edit": can_edit_note(note, current_user_id),
        "Username": username,
        "Date": date_str,
        "user_id": note.user_id
    }


# Adds a missing database column without deleting existing data.
def add_column_if_missing(table_name, column_name, column_definition):
    inspector = inspect(db.engine)
    existing_columns = [column["name"] for column in inspector.get_columns(table_name)]

    if column_name not in existing_columns:
        with db.engine.connect() as connection:
            connection.exec_driver_sql(
                f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
            )
            connection.commit()


# Registers a new user account.
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not name or not email or not password:
        return jsonify({"message": "All fields are required."}), 400

    if len(password) < 8:
        return jsonify({"message": "Password must be at least 8 characters."}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "Email already exists."}), 409

    new_user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password)
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201


# Logs in a user and returns a JWT access token.
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password."}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful.",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 200


# Creates a new note for the logged-in user.
@app.route("/api/notes", methods=["POST"])
@jwt_required()
def create_note():
    data = request.get_json()
    user_id = get_current_user_id()

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not all([
        data.get("title"),
        data.get("description"),
        data.get("subject"),
        data.get("fileLink")
    ]):
        return jsonify({"message": "All fields are required"}), 400

    try:
        links = serialize_links(data.get("links", []))
    except ValueError as error:
        return jsonify({"message": str(error)}), 400

    new_note = Note(
        title=data.get("title"),
        description=data.get("description"),
        subject=data.get("subject"),
        fileLink=data.get("fileLink"),
        links=links,
        editable_by_others=bool(data.get("editable_by_others", False)),
        user_id=user_id
    )

    db.session.add(new_note)
    db.session.commit()

    return jsonify({"message": "Note created successfully"}), 201


# Gets all notes for browsing.
@app.route("/api/notes", methods=["GET"])
@jwt_required(optional=True)
def get_notes():
    current_user_id = get_current_user_id()
    notes = Note.query.all()
    return jsonify([note_to_dict(note, current_user_id) for note in notes]), 200


# Gets only the notes created by the logged-in user.
@app.route("/api/my_notes", methods=["GET"])
@jwt_required()
def get_my_notes():
    current_user_id = get_current_user_id()
    notes = Note.query.filter_by(user_id=current_user_id).all()
    return jsonify([note_to_dict(note, current_user_id) for note in notes]), 200


# Updates a note and saves its previous state as a version.
@app.route("/api/notes/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    current_user_id = get_current_user_id()
    note = Note.query.get_or_404(note_id)

    if not can_edit_note(note, current_user_id):
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    editor = User.query.get(current_user_id)

    old_version = NoteVersion(
        note_id=note.id,
        title=note.title,
        description=note.description,
        subject=note.subject,
        fileLink=note.fileLink,
        links=note.links,
        editable_by_others=note.editable_by_others,
        edited_by=editor.name if editor else "Unknown"
    )

    db.session.add(old_version)

    note.title = data.get("title", note.title)
    note.description = data.get("description", note.description)
    note.subject = data.get("subject", note.subject)
    note.fileLink = data.get("fileLink", note.fileLink)

    if note.user_id == current_user_id and "editable_by_others" in data:
        note.editable_by_others = bool(data.get("editable_by_others"))

    if "links" in data:
        try:
            note.links = serialize_links(data.get("links"))
        except ValueError as error:
            return jsonify({"message": str(error)}), 400

    db.session.commit()

    return jsonify({"message": "Note updated successfully"}), 200


# Gets the version history of a note.
@app.route("/api/notes/<int:note_id>/versions", methods=["GET"])
@jwt_required()
def get_note_versions(note_id):
    current_user_id = get_current_user_id()
    note = Note.query.get_or_404(note_id)

    if not can_edit_note(note, current_user_id):
        return jsonify({"message": "Unauthorized"}), 403

    versions = NoteVersion.query.filter_by(note_id=note_id).order_by(
        NoteVersion.edited_at.desc()
    ).all()

    result = []

    for version in versions:
        result.append({
            "id": version.id,
            "note_id": version.note_id,
            "title": version.title,
            "description": version.description,
            "subject": version.subject,
            "fileLink": version.fileLink,
            "links": deserialize_links(version.links),
            "editable_by_others": bool(version.editable_by_others),
            "edited_at": version.edited_at.strftime("%b %d, %Y %I:%M %p") if version.edited_at else "",
            "edited_by": version.edited_by or "Unknown"
        })

    return jsonify(result), 200


# Restores a previous note version.
@app.route("/api/notes/<int:note_id>/versions/<int:version_id>/restore", methods=["PUT"])
@jwt_required()
def restore_note_version(note_id, version_id):
    current_user_id = get_current_user_id()
    note = Note.query.get_or_404(note_id)

    if not can_edit_note(note, current_user_id):
        return jsonify({"message": "Unauthorized"}), 403

    version = NoteVersion.query.filter_by(
        id=version_id,
        note_id=note_id
    ).first_or_404()

    editor = User.query.get(current_user_id)

    current_version = NoteVersion(
        note_id=note.id,
        title=note.title,
        description=note.description,
        subject=note.subject,
        fileLink=note.fileLink,
        links=note.links,
        editable_by_others=note.editable_by_others,
        edited_by=editor.name if editor else "Unknown"
    )

    db.session.add(current_version)

    note.title = version.title
    note.description = version.description
    note.subject = version.subject
    note.fileLink = version.fileLink
    note.links = version.links

    if note.user_id == current_user_id:
        note.editable_by_others = bool(version.editable_by_others)

    db.session.commit()

    return jsonify({"message": "Version restored successfully"}), 200


# Deletes a note and its saved versions.
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    current_user_id = get_current_user_id()
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403

    NoteVersion.query.filter_by(note_id=note.id).delete()
    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted successfully"}), 200


# Creates tables and adds missing columns.
def initialize_database():
    db.create_all()
    add_column_if_missing("notes", "links", "TEXT DEFAULT '[]'")
    add_column_if_missing("notes", "editable_by_others", "BOOLEAN DEFAULT 0")
    add_column_if_missing("note_versions", "links", "TEXT DEFAULT '[]'")
    add_column_if_missing("note_versions", "editable_by_others", "BOOLEAN DEFAULT 0")


with app.app_context():
    initialize_database()


if __name__ == "__main__":
    app.run(debug=True)