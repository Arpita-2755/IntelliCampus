import os
import uuid
from datetime import date

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from app.attendance import attendance
from app import db

from app.models.user import User
from app.models.attendance import Attendance

from ai_engine.attendance_marker import mark_attendance_from_image


UPLOAD_FOLDER = "temp_uploads"


# =====================================================
# MANUAL ATTENDANCE
# =====================================================

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

        # ===============================
        # AUTO RECALCULATE ATTENDANCE %
        # ===============================
        for student in students:

            total_classes = Attendance.query.filter_by(
                student_id=student.id
            ).count()

            presents = Attendance.query.filter_by(
                student_id=student.id,
                status="Present"
            ).count()

            percentage = (
                (presents / total_classes) * 100
                if total_classes > 0 else 0
            )

            student.attendance_percentage = round(percentage, 2)
            student.is_defaulter = percentage < 75

            # 🔥 SIMULATED EMAIL ALERT
            if student.is_defaulter:
                try:
                    from app.utils.email import send_defaulter_email
                    send_defaulter_email(student.email, student.name)
                except Exception as e:
                    print("EMAIL SIMULATION:", e)

        db.session.commit()

        flash("Attendance marked successfully ✅", "success")
        return redirect(url_for("dashboard.smart_dashboard"))

    return render_template("mark_attendance.html", students=students)


# =====================================================
# AI ATTENDANCE
# =====================================================

@attendance.route("/ai_attendance", methods=["GET", "POST"])
@login_required
def ai_attendance():

    # faculty + admin allowed
    if current_user.role not in ["faculty", "admin"]:
        flash("Unauthorized access.", "warning")
        return redirect(url_for("dashboard.smart_dashboard"))

    if request.method == "POST":

        image = request.files.get("class_image")

        if not image or image.filename == "":
            flash("Please upload a classroom image.", "warning")
            return redirect(request.url)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        filename = f"{uuid.uuid4()}.jpg"
        path = os.path.join(UPLOAD_FOLDER, filename)

        image.save(path)

        try:

            # ===============================
            # AI ATTENDANCE PIPELINE
            # ===============================
            present_students, absent_students = mark_attendance_from_image(
                path,
                current_user.id
            )

            # ===============================
            # RECALCULATE PERCENTAGES
            # ===============================
            from app.utils.attendance_utils import recalculate_attendance
            recalculate_attendance()

            flash("AI Attendance Completed ✅", "success")

            return render_template(
                "ai_result.html",
                present_students=present_students,
                absent_students=absent_students
            )

        except Exception as e:
            print("AI ERROR:", e)
            flash("AI attendance failed.", "danger")
            return redirect(url_for("dashboard.smart_dashboard"))

        finally:
            if os.path.exists(path):
                os.remove(path)

    return render_template("ai_attendance.html")