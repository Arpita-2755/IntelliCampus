import os
import uuid

from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from app.auth import auth
from app.models.user import User
from app import db

from deepface import DeepFace


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

        # 🔥 Prevent duplicate users (VERY IMPORTANT)
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered. Please login.")
            return redirect(url_for("auth.login"))

        hashed_password = generate_password_hash(password)

        face_filename = None
        embedding = None

        face = request.files.get("face")

# 🔥 FORCE FACE FOR STUDENTS
        if role == "student":
            if not face or face.filename == "":
                flash("Students must upload a face image for AI attendance.")
                return redirect(url_for("auth.register"))


        # 🔥 Only process face if uploaded
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
                print("EMBEDDING GENERATED:", len(embedding))
                face_filename = filename

                # ⭐ OPTIONAL BUT SMART:
                # Delete raw image after embedding to save storage
                # os.remove(filepath)

            except Exception:
                flash("Face not detected. Upload a clear front-face image.")
                return redirect(url_for("auth.register"))

        # 🔥 CREATE USER
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
