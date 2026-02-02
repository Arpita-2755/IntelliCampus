import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")


def send_defaulter_email(student_email, student_name):

    try:

        resend.Emails.send({
            "from": "IntelliCampus <onboarding@resend.dev>",
            "to": student_email,
            "subject": "Attendance Warning ⚠️",
            "html": f"""
                <h3>Hello {student_name}</h3>
                <p>Your attendance has fallen below <b>75%</b>.</p>
                <p>Please attend classes regularly.</p>
                <br>
                <p><i>IntelliCampus AI</i></p>
            """
        })

    except Exception as e:
        print("Email failed:", e)

