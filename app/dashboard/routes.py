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