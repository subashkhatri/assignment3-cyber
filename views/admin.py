from flask import Blueprint, render_template, request, session
from db import Messages
from db.base import db

app = Blueprint('admin', __name__, template_folder='templates')


@app.route("/admin", methods=["GET", "POST"])
def admin():
    is_admin = False
    # CB-05-001 Changes
    if 'username' in session and session.get('usertype') == 'admin':
        is_admin = True
    messages = Messages.query.all()
    return render_template(
        "admin.html",
        # cookies=request.cookies,
        is_admin=is_admin,
        messages=messages
    )
