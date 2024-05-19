from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, PasswordField, HiddenField
from wtforms.validators import InputRequired, EqualTo, Length

class CreateForm(FlaskForm):
    name = StringField("Name of Account: ", validators=[InputRequired(), Length(max=50)])
    balance = IntegerField("Opening balance (optional)", default=10)
    password = PasswordField(
        "Account password",
        validators=[InputRequired(), EqualTo("pwd_confirm", message="Passwords must match"), Length(max=50)]
    )
    pwd_confirm = PasswordField("Confirm account password", validators=[Length(max=50)])
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    id = StringField("Username: ", validators=[InputRequired(), Length(max=50)])
    password = PasswordField("Password: ", validators=[InputRequired(), Length(max=50)])
    submit = SubmitField("Login")

class WithdrawForm(FlaskForm):
    amount = FloatField("Withdraw Amount: ", validators=[InputRequired()])
    description = StringField("Description: ", validators=[InputRequired(), Length(max=100)])
    withdraw = SubmitField("Withdraw Amount")

class MessageForm(FlaskForm):
    message_text = StringField("Your Message: ", validators=[InputRequired(), Length(max=200)])
    message = SubmitField("Send")

class TransferForm(FlaskForm):
    account_id = IntegerField("Recipient's Account ID: ", validators=[InputRequired()])
    amount = FloatField("Transfer Amount: ", validators=[InputRequired()])
    transfer = SubmitField("Transfer Amount")
    transfer_from = IntegerField("Transfer From")

class DeleteForm(FlaskForm):
    id = IntegerField("Account ID to Delete: ", validators=[InputRequired()])
    password = PasswordField(
        "Account password: ",
        validators=[InputRequired(), EqualTo("pwd_confirm", message="Passwords must match"), Length(max=50)]
    )
    pwd_confirm = PasswordField("Confirm account password: ", validators=[Length(max=50)])
    submit = SubmitField("Delete Account")
    admin = HiddenField("is admin", default="false")
