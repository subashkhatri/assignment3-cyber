import re
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, current_app
from sqlalchemy import text
from logic.forms import (
    CreateForm,
    LoginForm
)
from db import Transaction, Account
from db.base import db

app = Blueprint('accounts', __name__, template_folder='templates')


def is_valid_input(input_string):  # CB-06-001
    return re.match("^[A-Za-z0-9 ]*$", input_string) is not None


@app.route("/create", methods=["GET", "POST"])
def create_account():
    form = CreateForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        new_account = Account(name, password, 100)
        db.session.add(new_account)
        db.session.commit()
        new_transaction = Transaction(
            "Balance Add.", "Rewards account opened.", new_account.id, 100
        )
        db.session.add(new_transaction)
        db.session.commit()
        session["username"] = new_account.name

        return redirect(url_for("display.my_account"))

    return render_template("create_account.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.id.data
        password = form.password.data
        user = None
        if "'" in user_id:
            return "<h1>STOP TRYING TO HACK US</h1>"
        try:
            if not re.match("^[0-9]+$", user_id):  # CB-04-001 changes
                return "<h1>Invalid user ID. Must be an integer.</h1>"
            id = int(user_id)
        except:
            return "<h1>Invalid user ID. Must be an integer.</h1>"

        with db.get_engine().connect() as con:
            for row in con.execute(
                text("SELECT name, password FROM accounts where id  = :id"),
                {'id': id}  # CB-04-001 changes
            ):
                user = row
        if password == user[1]:  # CB-01-001 changes
            if user:
                session["username"] = user[0]
                # session["usertype"] = "admin"
                return redirect(url_for("display.my_account"))
        else:
            return "<h1>Invalid Account ID & Password combination</h1>"

    return render_template("login.html", form=form)


@ app.route("/logout", methods=["GET"])
def logout():
    session["username"] = None
    session.clear()  # CB-05-001 Changes
    return redirect(url_for("base.index"))


@ app.route("/json/account/name")
def json_names():
    name = request.args.get("name")

    if not name:
        return jsonify({"name": "must specify name"})

    if not is_valid_input(name):  # CB-04-001 changes
        return jsonify({"error": "Invalid input"}), 400

    userObj = None

    with db.get_engine().connect() as con:
        result = con.execute(
            text("SELECT * FROM accounts WHERE name = :name"),
            {'name': name}  # CB-04-001 changes
        )
        userObj = result.fetchone()

    if userObj:
        if current_app.config["app_debug"]:  # CB-01-002 changes
            return jsonify({"DEBUG": str(userObj)})
        return jsonify({"name": "taken"})
    else:
        return jsonify({"name": "available"})


@ app.route("/json/account/id")
def json_account_id():
    account_id = request.args.get("account_id")
    if not account_id:
        return jsonify({"name": "must specify name"})

    if not re.match("^[0-9]+$", account_id):  # CB-04-001 changes
        return jsonify({"error": "Invalid account ID"}), 400

    userObj = None

    with db.get_engine().connect() as con:
        result = con.execute(
            text("SELECT * FROM accounts WHERE id = :account_id"),
            {'account_id': account_id}  # CB-04-001 changes
        )
        userObj = result.fetchone()

    if userObj:
        if current_app.config["app_debug"]:  # CB-01-002 changes
            return jsonify({"DEBUG": str(userObj)})
        return jsonify({"account": "valid"})
    else:
        return jsonify({"account": "invalid"})
