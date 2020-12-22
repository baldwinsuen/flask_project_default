from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import jwt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    """ User Model """

    __tablename__ = "UserModel"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __init__(self, firstname, lastname, username, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password  # look into Flask.Bcrypt if you get the chance

    def encode_auth_token(self, user_id):
        """ Generates authentication token """

        try:
            payload = {
                # exp -> expiration date | iat -> token creation date | sub -> subject of token
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=0, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, app.config.get("SECRET_KEY"), algorithm="HS256")

        except Exception as e:
            return e


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
