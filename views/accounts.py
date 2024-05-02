import re
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from sqlalchemy import text
from logic.forms import (
    CreateForm,
    LoginForm
)
from db import Transaction, Account
from db.base import db

app = Blueprint('accounts', __name__, template_folder='templates')


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
            id = int(user_id)
        except:
            return "<h1>Invalid user ID. Must be an integer.</h1>"
    
        with db.get_engine().connect() as con:
            for row in con.execute(
                text(
                    f"SELECT name, password FROM accounts where id ='{id}' LIMIT 1"
                )
            ):
                user = row
        if re.search(f"{password}", user[1]):
            if user:
                session["username"] = user[0]
                return redirect(url_for("display.my_account"))
        else:
            return "<h1>Invalid Account ID & Password combination</h1>"

    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    session["username"] = None
    return redirect(url_for("base.index"))


@app.route("/json/account/name")
def json_names():
    name = request.args.get("name")
    if not name:
        return jsonify({"name": "must specify name"})
    userObj = None
    with db.get_engine().connect() as con:
            for row in con.execute(
                text(
                    f"SELECT * FROM accounts where name = '{name}'"
                )
            ):
                userObj = row
    if userObj:
        if request.args.get("debug") == "true":
            return jsonify({"DEBUG": str(userObj)})
        return jsonify({"name": "taken"})
    else:
        return jsonify({"name": "available"})


@app.route("/json/account/id")
def json_account_id():
    account_id = request.args.get("account_id")
    if not account_id:
        return jsonify({"name": "must specify name"})
    userObj = None
    with db.get_engine().connect() as con:
            for row in con.execute(
                text(
                    f"SELECT * FROM accounts where id = '{account_id}'"
                )
            ):
                userObj = row
    if userObj:
        if request.args.get("debug") == "true":
            return jsonify({"DEBUG": str(userObj)})
        return jsonify({"account": "valid"})
    else:
        return jsonify({"account": "invalid"})
