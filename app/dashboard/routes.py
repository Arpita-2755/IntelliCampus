from flask_login import login_required, current_user
from flask import render_template
from app.dashboard import dashboard


@dashboard.route("/dashboard")
@login_required
def smart_dashboard():

    if current_user.role == "admin":
        return render_template("admin_dashboard.html")

    elif current_user.role == "faculty":
        return render_template("faculty_dashboard.html")

    elif current_user.role == "student":
        return render_template("student_dashboard.html")

from app.models.user import User


@dashboard.route("/defaulters")
@login_required
def defaulters():

    if current_user.role != "admin":
        return "<h3>Access Denied</h3>"

    defaulters = User.query.filter_by(is_defaulter=True).all()

    return render_template("defaulters.html", defaulters=defaulters)

from app.models.attendance import Attendance


@dashboard.route("/analytics")
@login_required
def analytics():

    if current_user.role != "admin":
        return "<h3>Access Denied</h3>"

    presents = Attendance.query.filter_by(status="Present").count()
    absents = Attendance.query.filter_by(status="Absent").count()

    return render_template(
        "analytics.html",
        presents=presents,
        absents=absents
    )
