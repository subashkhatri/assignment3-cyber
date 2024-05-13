from flask import Flask
from db.base import db
from flask_migrate import Migrate

# Import views
from views.accounts import app as accounts_view
from views.base import app as base_view
from views.display import app as display_view
from views.admin import app as admin_view

app = Flask(__name__)
app.register_blueprint(accounts_view)
app.register_blueprint(base_view)
app.register_blueprint(display_view)
app.register_blueprint(admin_view)

app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["DEBUG"] = True

db.init_app(app)
Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
