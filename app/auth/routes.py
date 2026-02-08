import os
import uuid

from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from app.auth import auth
from app.models.user import User
from app import db

from deepface import DeepFace
from ai_engine.faiss_manager import add_embedding

UPLOAD_FOLDER = "app/static/faces"


# ✅ HOME
@auth.route("/")
def home():
    return "<h1>IntelliCampus is Running 🚀</h1>"


# ✅ REGISTER
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        # ✅ Prevent duplicate users
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered. Please login.")
            return redirect(url_for("auth.login"))

        hashed_password = generate_password_hash(password)

        face_filename = None
        embedding = None

        face = request.files.get("face")

        # 🔥 Force face for students
        if role == "student":
            if not face or face.filename == "":
                flash("Students must upload a face image.")
                return redirect(url_for("auth.register"))

        # ✅ Process face if uploaded
        if face and face.filename != "":

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filename = f"{uuid.uuid4()}.jpg"
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            face.save(filepath)

            try:
                result = DeepFace.represent(
                    img_path=filepath,
                    model_name="Facenet",
                    enforce_detection=True
                )

                embedding = result[0]["embedding"]
                face_filename = filename

                print("EMBEDDING GENERATED:", len(embedding))

            except Exception as e:
                print("FACE ERROR:", e)
                flash("Face not detected. Upload a clear front-face image.")
                return redirect(url_for("auth.register"))

        # ✅ CREATE USER (ONLY ONCE — VERY IMPORTANT)
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            face_image=face_filename,
            embedding=embedding
        )

        db.session.add(user)
        db.session.commit()

        print("USER CREATED:", user.id)

        # ✅ ADD TO FAISS
        if embedding is not None:
            try:
                print("ADDING TO FAISS:", user.id)
                add_embedding(embedding, user.id)
            except Exception as e:
                print("FAISS ERROR:", e)

        flash("Registration successful! Please login.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")



# ✅ LOGIN
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User not found.")
            return redirect(url_for("auth.login"))

        if not check_password_hash(user.password, password):
            flash("Incorrect password.")
            return redirect(url_for("auth.login"))

        login_user(user)

        return redirect(url_for("dashboard.smart_dashboard"))

    return render_template("login.html")


# ✅ LOGOUT
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
