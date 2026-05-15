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

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notehub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)


db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})


# User Model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Note Model
class Note(db.Model):
   __tablename__ = "notes"

   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), nullable=False)
   description = db.Column(db.Text)
   subject = db.Column(db.String(100))
   fileLink = db.Column(db.String(100))
   links = db.Column(db.Text, default="[]")
   user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
   date_created = db.Column(db.DateTime, server_default=db.func.now())
 
   user = db.relationship("User", backref="notes")

# Note Version History Model
class NoteVersion(db.Model):
   __tablename__ = "note_versions"

   id = db.Column(db.Integer, primary_key=True)
   note_id = db.Column(db.Integer, db.ForeignKey("notes.id"), nullable=False)
   title = db.Column(db.String(100), nullable=False)
   description = db.Column(db.Text)
   subject = db.Column(db.String(100))
   fileLink = db.Column(db.String(100))
   links = db.Column(db.Text, default="[]")
   edited_at = db.Column(db.DateTime, server_default=db.func.now())
   edited_by = db.Column(db.String(100))
   note = db.relationship("Note", backref="versions")

# Register Route
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

    hashed_password = generate_password_hash(password)

    new_user = User(
        name=name,
        email=email,
        password_hash=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201


# Login Route
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

def is_valid_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ("http", "https") and bool(parsed_url.netloc)

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

def serialize_links(raw_links):
    return json.dumps(normalize_links(raw_links))

def deserialize_links(links_json):
    if not links_json:
        return []

    try:
        links = json.loads(links_json)
    except (TypeError, json.JSONDecodeError):
        return []

    return links if isinstance(links, list) else []

def note_to_dict(note):
    username = note.user.name if note.user else "Unknown"
    date_str = note.date_created.strftime("%b %d, %Y") if note.date_created else ""
    return {
        "id": note.id,
        "title": note.title,
        "description": note.description,
        "subject": note.subject,
        "fileLink": note.fileLink,
        "links": deserialize_links(note.links),
        "Username": username,
        "Date": date_str,
        "user_id": note.user_id
    }

def add_column_if_missing(table_name, column_name, column_definition):
    inspector = inspect(db.engine)
    existing_columns = [column["name"] for column in inspector.get_columns(table_name)]

    if column_name not in existing_columns:
        with db.engine.connect() as connection:
            connection.exec_driver_sql(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
            connection.commit()

# Creating a Note
@app.route("/api/notes", methods=["POST"])
@jwt_required()
def create_note():
    try:
        data = request.get_json()
        print("Received data:", data)

        user_id = get_jwt_identity()
        print("JWT user_id:", user_id)

        # Check if user actually exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Check all required fields
        if not all([data.get("title"), data.get("description"), data.get("subject"), data.get("fileLink")]):
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
            user_id=user_id
        )

        db.session.add(new_note)
        db.session.commit()
        print("Note created successfully!")

        return jsonify({"message": "Note created successfully"}), 201

    except Exception as e:
        # Print full traceback to console
        import traceback
        traceback.print_exc()
        return jsonify({"message": "Internal Server Error: " + str(e)}), 500

# Display Note
@app.route("/api/notes", methods=["GET"])
def get_notes():
    notes = Note.query.all()
    result = [note_to_dict(note) for note in notes]
    return jsonify(result)

# Display My Notes
@app.route("/api/my_notes", methods=["GET"])
@jwt_required()
def get_my_notes():
    current_user_id = get_jwt_identity()
    notes = Note.query.filter_by(user_id=current_user_id).all()
    
    result = [note_to_dict(note) for note in notes]

    return jsonify(result)

# Update Note
@app.route("/api/notes/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    current_user_id = int(get_jwt_identity())
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user_id:
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
    edited_by=editor.name if editor else "Unknown"
)
    db.session.add(old_version)

    note.title = data.get("title", note.title)
    note.description = data.get("description", note.description)
    note.subject = data.get("subject", note.subject)
    note.fileLink = data.get("fileLink", note.fileLink)
    if "links" in data:
        try:
            note.links = serialize_links(data.get("links"))
        except ValueError as error:
            return jsonify({"message": str(error)}), 400

    db.session.commit()

    return jsonify({"message": "Note updated successfully"}), 200

# Get Note Version History
@app.route("/api/notes/<int:note_id>/versions", methods=["GET"])
@jwt_required()
def get_note_versions(note_id):
    current_user_id = int(get_jwt_identity())
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403

    versions = NoteVersion.query.filter_by(note_id=note_id).order_by(NoteVersion.edited_at.desc()).all()

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
            "edited_at": version.edited_at.strftime("%b %d, %Y %I:%M %p") if version.edited_at else "",
            "edited_by": version.edited_by or "Unknown"
        })

    return jsonify(result), 200

# Restore Note Version
@app.route("/api/notes/<int:note_id>/versions/<int:version_id>/restore", methods=["PUT"])
@jwt_required()
def restore_note_version(note_id, version_id):
    current_user_id = int(get_jwt_identity())
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403

    version = NoteVersion.query.filter_by(id=version_id, note_id=note_id).first_or_404()

    editor = User.query.get(current_user_id)

    current_version = NoteVersion(
    note_id=note.id,
    title=note.title,
    description=note.description,
    subject=note.subject,
    fileLink=note.fileLink,
    links=note.links,
    edited_by=editor.name if editor else "Unknown"
)

    db.session.add(current_version)

    note.title = version.title
    note.description = version.description
    note.subject = version.subject
    note.fileLink = version.fileLink
    note.links = version.links

    db.session.commit()

    return jsonify({"message": "Version restored successfully"}), 200
# Delete Note
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    current_user_id = int(get_jwt_identity())
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted successfully"}), 200

def initialize_database():
    db.create_all()
    add_column_if_missing("notes", "links", "TEXT DEFAULT '[]'")
    add_column_if_missing("note_versions", "links", "TEXT DEFAULT '[]'")

with app.app_context():
    initialize_database()

if __name__ == "__main__":
    app.run(debug=True)
