from db.base import db
from datetime import datetime

# Database ORM for Transactions
class Transaction(db.Model):
    __tablename__ = "rewards"
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.Text)
    description = db.Column(db.Text)
    statement_description = db.Column(db.Text)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    account = db.relationship("Account", backref=db.backref("transactions", lazy=True))

    def __init__(
        self, transaction_type, description, account_id, statement=None, amount=0
    ):
        self.transaction_type = transaction_type
        self.description = description
        self.account_id = account_id
        self.amount = amount
        self.statement_description = statement

    def __repr__(self):
        return f"Transaction {self.id}: {self.transaction_type} on {self.date}"