# pylint: disable=no-member

from flask import Flask, redirect, url_for, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_login import login_user, login_required, logout_user, current_user

from forms import LoginForm, RegisterForm
from models import db, User, ToDO, login_manager

# Flask
app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00"
app.config["DEBUG"] = True

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True
login_manager.init_app(app)
db.init_app(app)
db.create_all()

bootstrap = Bootstrap(app)

# flask_login needs to retrieve unique id of the user
# will create session that is unique to the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["POST", "GET"])
def index():
    """ Home page """
    return render_template("index.html")


@app.route("/todo")
@login_required
def todo():
    """ TODO page """
    return render_template("todo.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    """ Login page and function """
    form = LoginForm()

    # if attempting to login
    if form.validate_on_submit():

        # check if user exists
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):

                # create session
                login_user(user, remember=form.remember.data)
                return render_template("todo.html")

    return render_template("login.html", form=form)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """ Signup page and function """
    form = RegisterForm()

    if form.validate_on_submit():

        # check if email or username is already in the database
        exists_email = (
            db.session.query(User.id).filter_by(email=form.email.data).scalar()
        )
        exists_username = (
            db.session.query(User.id).filter_by(username=form.username.data).scalar()
        )
        if exists_email or exists_username:
            return render_template("signup.html", form=form)

        # hash the password then add it to the database
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return render_template("index.html")

    return render_template("signup.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=3000)
