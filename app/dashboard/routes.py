from flask_login import login_required, current_user
from flask import render_template
from app.dashboard import dashboard

from app.models.user import User
from app.models.attendance import Attendance


@dashboard.route("/dashboard")
@login_required
def smart_dashboard():

    # ===== ADMIN DASHBOARD =====
    if current_user.role == "admin":

        total_students = User.query.filter_by(role="student").count()
        total_faculty = User.query.filter_by(role="faculty").count()
        defaulters = User.query.filter_by(is_defaulter=True).count()
        total_attendance = Attendance.query.count()

        return render_template(
            "admin_dashboard.html",
            total_students=total_students,
            total_faculty=total_faculty,
            defaulters=defaulters,
            total_attendance=total_attendance
        )

    # ===== FACULTY DASHBOARD =====
    elif current_user.role == "faculty":

        history = Attendance.query.filter_by(
            faculty_id=current_user.id
        ).order_by(Attendance.created_at.desc()).limit(15).all()

        return render_template(
            "faculty_dashboard.html",
            history=history
        )

    # ===== STUDENT DASHBOARD =====
    elif current_user.role == "student":

        history = Attendance.query.filter_by(
            student_id=current_user.id
        ).order_by(Attendance.created_at.desc()).all()

        return render_template(
            "student_dashboard.html",
            history=history
        )


@dashboard.route("/defaulters")
@login_required
def defaulters():

    if current_user.role != "admin":
        return "<h3>Access Denied</h3>"

    defaulters = User.query.filter_by(is_defaulter=True).all()

    return render_template("defaulters.html", defaulters=defaulters)


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