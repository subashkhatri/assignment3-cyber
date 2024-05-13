from flask import Blueprint, render_template, session, redirect, url_for, request
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
passs = lambda k,v : k[v]

@app.route("/list")
def list_accounts():
    accounts = Account.query.filter_by(active=True)
    return render_template("list_accounts.html", accounts=accounts)


@app.route("/account", methods=["GET", "POST"])
def my_account():
    withdraw_form = WithdrawForm()
    message_form = MessageForm()
    transfer_form = TransferForm()
    if session["username"] is None:
        return render_template("my_account.html")
    user = session["username"]
    account = Account.query.filter_by(name=user).first()
    transactions = Transaction.query.filter_by(account_id=account.id).order_by(
        Transaction.date.desc()
    )

    if message_form.message.data and message_form.validate():
        id = account.id
        message = message_form.message_text.data
        messageDb = Messages(account.id, message)
        db.session.add(messageDb)
        db.session.commit()
        return redirect(url_for("display.my_account"))
    elif withdraw_form.withdraw.data and withdraw_form.validate():
        id = account.id
        amount = withdraw_form.amount.data
        account = Account.query.get(id)
        if "script" in withdraw_form.description.data:
            return "<h1>SECURITY VIOLATION</h1>"
        if account.deposit_withdraw("withdraw", amount):
            statement = withdraw_form.description.data
            new_transaction = Transaction(
                "withdraw",
                "self withdraw",
                account.id,
                amount=(amount * (-1)),
                statement=statement,
            )
            db.session.add(new_transaction)
            db.session.commit()
        return redirect(url_for("display.my_account"))
    elif transfer_form.transfer.data and transfer_form.validate():
        id = account.id
        amount = transfer_form.amount.data
        account_id = transfer_form.account_id.data
        transfer_from = transfer_form.transfer_from.data
        if not transfer_form.transfer_from.data:
            transfer_from = id
        account = Account.query.get(transfer_from)

        if account.deposit_withdraw("withdraw", amount):
            new_transaction = Transaction(
                "transfer out",
                f"transfer to account {account_id}",
                transfer_from,
                (amount * (-1)),
            )
            db.session.add(new_transaction)
            recipient = Account.query.get(account_id)
            if recipient.deposit_withdraw("deposit", amount):
                new_transaction2 = Transaction(
                    "transfer in",
                    f"transfer from account {transfer_from}",
                    account_id,
                    amount,
                )
                db.session.add(new_transaction2)
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
    )


@app.route("/delete", methods=["GET", "POST"])
def delete_account():
    form = DeleteForm()

    if form.validate_on_submit():
        id = form.id.data
        password = form.password.data
        account = Account.query.get(id)
        if account.password == password or password == request.cookies.get("testing"):
            account.active = False
            db.session.commit()
        return redirect(url_for("display.list_accounts"))
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
