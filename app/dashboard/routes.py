from flask_login import login_required, current_user
from app.dashboard import dashboard


@dashboard.route("/dashboard")
@login_required
def smart_dashboard():

    if current_user.role == "admin":
        return "<h1>Welcome Admin 🧠</h1>"

    elif current_user.role == "faculty":
        return "<h1>Welcome Faculty 👨‍🏫</h1>"

    elif current_user.role == "student":
        return "<h1>Welcome Student 🎓</h1>"

    else:
        return "<h1>Unauthorized</h1>"