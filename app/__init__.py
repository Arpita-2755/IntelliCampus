from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # ✅ CREATE DATABASE TABLES
    with app.app_context():
        from app.models import User, Attendance
        db.create_all()

    # ✅ REGISTER BLUEPRINTS
    from app.auth import auth
    from app.dashboard import dashboard
    from app.attendance import attendance

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(attendance)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))
