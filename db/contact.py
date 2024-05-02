from db.base import db
from datetime import datetime

# Database ORM for Transactions
class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    account = db.relationship("Account", backref=db.backref("messages", lazy=True))

    def __init__(
        self, account_id, message
    ):
        self.account_id = account_id
        self.message = message