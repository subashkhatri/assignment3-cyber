import re
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from logic.forms import (
    MessageForm,
    TransferForm,
    WithdrawForm,
    DeleteForm
)
from db import Transaction, Account, Messages
from db.base import db
import json
import requests

app = Blueprint('display', __name__, template_folder='templates')
def passs(k, v): return k[v]


def is_valid_input(input_string):
    return re.match("^[A-Za-z0-9 ]*$", input_string) is not None


@app.route("/list")
def list_accounts():
    accounts = Account.query.filter_by(active=True)
    return render_template("list_accounts.html", accounts=accounts)


@app.route("/account", methods=["GET", "POST"])
def my_account():
    if "username" not in session:
        return redirect(url_for("login"))

    user = session["username"]
    account = Account.query.filter_by(name=user).first()
    transactions = Transaction.query.filter_by(
        account_id=account.id).order_by(Transaction.date.desc())

    withdraw_form = WithdrawForm()
    message_form = MessageForm()
    transfer_form = TransferForm()
    error_message = ""

    if message_form.validate_on_submit():
        if not is_valid_input(message_form.message_text.data):
            print('Invalid text detected')
            error_message = "Invalid input"
        else:
            messageDb = Messages(account_id=account.id,
                                 message=message_form.message_text.data)
            db.session.add(messageDb)
            db.session.commit()
            return redirect(url_for("display.my_account"))

    if withdraw_form.validate_on_submit():
        if account.deposit_withdraw("withdraw", withdraw_form.amount.data):
            new_transaction = Transaction(
                type="withdraw",
                description=withdraw_form.description.data,
                account_id=account.id,
                amount=-withdraw_form.amount.data
            )
            db.session.add(new_transaction)
            db.session.commit()
        return redirect(url_for("display.my_account"))

    if transfer_form.validate_on_submit():
        transfer_from = transfer_form.transfer_from.data if transfer_form.transfer_from.data else account.id
        recipient = Account.query.get(transfer_form.account_id.data)

        if account.deposit_withdraw("withdraw", transfer_form.amount.data) and recipient:
            account.deposit_withdraw("withdraw", transfer_form.amount.data)
            recipient.deposit_withdraw("deposit", transfer_form.amount.data)
            db.session.add(Transaction(
                type="transfer",
                description=f"Transfer to account {recipient.id}",
                account_id=transfer_from,
                amount=-transfer_form.amount.data
            ))
            db.session.add(Transaction(
                type="deposit",
                description=f"Transfer from account {account.id}",
                account_id=recipient.id,
                amount=transfer_form.amount.data
            ))
            db.session.commit()
        return redirect(url_for("display.my_account"))

    return render_template(
        "my_account.html",
        user=user,
        account=account,
        transactions=transactions,
        withdraw_form=withdraw_form,
        message_form=message_form,
        transfer_form=transfer_form,
        error_message=error_message
    )


@app.route("/delete", methods=["GET", "POST"])
def delete_account():
    form = DeleteForm()

    if form.validate_on_submit():
        id = form.id.data
        password = form.password.data
        account = Account.query.get(id)

        if account and account.password == password:
            account.active = False
            db.session.commit()
            return redirect(url_for("display.list_accounts"))
        else:
            return redirect(url_for("delete_account"))

    return render_template("delete_account.html", form=form)


@app.route("/pong", methods=["GET"])
def pong():
    return "pong"


@app.route("/ping", methods=["GET"])
def ping():
    data = json.loads(str(request.args.to_dict()).replace("'", '"'))
    data = data.get("u") if data.get("u") else "http://localhost:5000/pong"
    try:
        return requests.get(data).text
    except:
        return "error ping"
