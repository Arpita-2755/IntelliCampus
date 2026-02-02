from flask_login import login_required, current_user
from flask import render_template, request
from datetime import date

from app.attendance import attendance
from app.models.user import User
from app.models.attendance import Attendance
from app import db


@attendance.route("/mark_attendance", methods=["GET", "POST"])
@login_required
def mark_attendance():

    if current_user.role != "faculty":
        return "<h3>Access Denied</h3>"

    students = User.query.filter_by(role="student").all()

    if request.method == "POST":

        for student in students:

            status = request.form.get(str(student.id))

            record = Attendance(
                student_id=student.id,
                faculty_id=current_user.id,
                date=date.today(),
                status=status
            )

            db.session.add(record)

        db.session.commit()

        return "<h2>Attendance Marked Successfully ✅</h2>"

    return render_template("mark_attendance.html", students=students)