from app import db
from app.models.user import User
from app.models.attendance import Attendance

from ai_engine.multi_face_attendance import process_class_image
from datetime import date


def mark_attendance_from_image(image_path, faculty_id):

    present_ids = process_class_image(image_path)
    


    # Get all students
    students = User.query.filter_by(role="student").all()

    for student in students:
        existing = Attendance.query.filter_by(
            student_id=student.id,
            date=date.today()
        ).first()

        if existing:
            continue

        status = "Present" if student.id in present_ids else "Absent"

        attendance = Attendance(
            student_id=student.id,
            faculty_id=faculty_id,
            date=date.today(),
            status=status
        )

        db.session.add(attendance)
    db.session.commit()

    present_students = [s for s in students if s.id in present_ids]
    absent_students = [s for s in students if s.id not in present_ids]

    return present_students, absent_students

