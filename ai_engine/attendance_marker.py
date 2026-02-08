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
    print("PRESENT IDS:", present_ids)

    return len(present_ids)
