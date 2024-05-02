from flask import Flask
from flask_migrate import Migrate
from flask import Flask
from sqlalchemy import text
from db.base import db

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
    # START OF OUT OF SCOPE
    # THIS IS OUT OF SCOPE. THIS STATEMENT IS USED TO FILL DEFAULT CONTENT
    with db.get_engine().connect() as con:
        con.execute(text("INSERT INTO accounts(id, name, password, balance, active) select 1, 'carter', '8ea8bc2d', 10000, 1 WHERE NOT EXISTS (select id from accounts where id = 1);"))
    # END OF OUT OF SCOPE
    app.run(debug=True, host="0.0.0.0", port=5000)
