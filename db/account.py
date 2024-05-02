from db.base import db

# Database ORM for Account
class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.Text)  # To be HASHED
    balance = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)

    def deposit_withdraw(self, type, amount):
        if type == "withdraw":
            amount *= -1
        if self.balance + amount < 0:
            return False  # Unsuccessful
        self.balance += amount
        return True  # Successful

    def __init__(self, name, password, balance=0):
        self.name = name
        self.password = password
        self.balance = balance

    def __repr__(self):
        return f"Account name is {self.name} with account number {self.id}"