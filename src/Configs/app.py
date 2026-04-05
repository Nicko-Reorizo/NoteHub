from datetime import timedelta

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
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
   user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
   date_created = db.Column(db.DateTime, server_default=db.func.now())
 
   user = db.relationship("User", backref="notes")


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

        new_note = Note(
            title=data.get("title"),
            description=data.get("description"),
            subject=data.get("subject"),
            fileLink=data.get("fileLink"),
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
    result = []
    for note in notes:
        username = "Unknown"
        if note.user:
            username = note.user.name
        date_str = note.date_created.strftime("%b %d, %Y") if note.date_created else ""
        result.append({
            "id": note.id,
            "title": note.title,
            "description": note.description,
            "subject": note.subject,
            "fileLink": note.fileLink,
            "Username": username,
            "Date": date_str
        })
    return jsonify(result)

# Display My Notes
@app.route("/api/my_notes", methods=["GET"])
@jwt_required()  # User must be logged in
def get_my_notes():
    current_user_id = get_jwt_identity()  # Get logged-in user's ID
    notes = Note.query.filter_by(user_id=current_user_id).all()
    
    result = []
    for note in notes:
        
        result.append({
            "id": note.id,
            "title": note.title,
            "description": note.description,
            "subject": note.subject,
            "fileLink": note.fileLink,
            "Username": note.user.name if note.user else "Unknown",
            "Date": note.date_created.strftime("%b %d, %Y") if note.date_created else ""
        })
    return jsonify(result)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)