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
        self.password = password  # look into Flask.Bcrypt if you get the chance


class ToDO(db.Model):
    """ TODO Model """

    __tablename__ = "TODOModel"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    due_date = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, description, due_date):
        self.name = name
        self.description = description
        self.due_date = datetime.utcnow()

    def __repr__(self):
        return "<Task %r>" % self.id
