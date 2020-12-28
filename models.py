# pylint: disable=no-member

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = "login"


class Todo(db.Model):
    """ TODO Model """

    __tablename__ = "TODOModel"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    date_created = db.Column(db.Date, default=datetime.now().date())
    owner = db.Column(db.String(32), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, content, due_date, owner):
        self.content = content
        self.due_date = due_date
        self.date_created = datetime.now().date()
        self.owner = owner


class User(UserMixin, db.Model):
    """ User Model """

    __tablename__ = "UserModel"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
