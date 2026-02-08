from app.models.user import User
from app.models.attendance import Attendance
from app import db


def recalculate_attendance():

    students = User.query.filter_by(role="student").all()

    for student in students:

        total_classes = Attendance.query.filter_by(
            student_id=student.id
        ).count()

        presents = Attendance.query.filter_by(
            student_id=student.id,
            status="Present"
        ).count()

        percentage = (presents / total_classes) * 100 if total_classes > 0 else 0

        student.attendance_percentage = round(percentage, 2)

        student.is_defaulter = percentage < 75

    db.session.commit()
