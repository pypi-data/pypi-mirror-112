from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/ttsi.db'
secret_key = os.environ['SECRET_KEY']

if not secret_key:
    tmp_file = "/tmp/ttsi_secret.txt"
    try:
        secret_key = open("/tmp/ttsi_secret.txt", "r").read()
    except FileNotFoundError:
        secret_key = secrets.token_urlsafe(16)
        f = open(tmp_file, "w")
        f.write(secret_key)
        f.close()

app.config['SECRET_KEY'] = s

db = SQLAlchemy(app)


@app.route("/")
def index():
    return "Hello World!"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


admin = Admin(app)
admin.add_view(ModelView(User, db.session))
