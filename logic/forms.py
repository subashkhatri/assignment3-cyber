from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    FloatField,
    PasswordField,
    HiddenField,
)
from wtforms.validators import InputRequired, EqualTo


class CreateForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField("Name of Account: ", [InputRequired()])
    balance = IntegerField("Opening balance (optional)", default=10)
    password = PasswordField(
        "Account password",
        [InputRequired(), EqualTo("pwd_confirm", message="Passwords must match")],
    )
    pwd_confirm = PasswordField("Confirm account password")
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    id = StringField("Username: ", [InputRequired()])
    password = PasswordField("Password: ", [InputRequired()])
    submit = SubmitField("Login")


class WithdrawForm(FlaskForm):
    class Meta:
        csrf = False

    amount = FloatField("Withdraw Amount: ", [InputRequired()])
    description = StringField("Description: ", [InputRequired()])
    withdraw = SubmitField("Withdraw Amount")


class MessageForm(FlaskForm):
    class Meta:
        csrf = False

    message_text = StringField("Your Message: ", [InputRequired()])
    message = SubmitField("Send")


class TransferForm(FlaskForm):
    class Meta:
        csrf = False

    account_id = IntegerField("Recipient's Account ID: ", [InputRequired()])
    amount = FloatField("Transfer Amount: ", [InputRequired()])
    transfer = SubmitField("Transfer Amount")
    transfer_from = IntegerField("transfer_from")


class DeleteForm(FlaskForm):
    class Meta:
        csrf = False

    id = IntegerField("Account ID to Delete: ", [InputRequired()])
    password = PasswordField(
        "Account password: ",
        [InputRequired(), EqualTo("pwd_confirm", message="Passwords must match")],
    )
    pwd_confirm = PasswordField("Confirm account password: ")
    submit = SubmitField("Delete Account")
    admin = HiddenField("is admin", default="false")
