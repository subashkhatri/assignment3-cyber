from flask import Blueprint, render_template, request
from db import Messages
from db.base import db

app = Blueprint('admin', __name__, template_folder='templates')

@app.route("/admin", methods=["GET", "POST"])
def admin():
    messages = Messages.query.all()
    return render_template(
        "admin.html",
        cookies=request.cookies,
        messages=messages
    )
