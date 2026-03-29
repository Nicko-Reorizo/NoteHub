from datetime import timedelta

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notehub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Allow Vue frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})


# User Model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)