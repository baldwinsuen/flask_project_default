from flask import Flask, redirect, url_for, render_template, request
from models import db, User, ToDO

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
db.init_app(app)

db.create_all()


@app.route("/", methods=["POST", "GET"])
def index():
    """ Home page """

    return render_template("index.html")


@app.route("/todo")
def todo():
    """ TODO page """
    return render_template("todo.html")


@app.route("/login")
def login():
    """ Login page and function """
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """ Signup page and function """

    if request.method == "POST":
        form_firstname = request.form.get("firstname")
        form_lastname = request.form.get("lastname")
        form_username = request.form.get("username")
        form_password = request.form.get("password")

        check_user = User.query.filter_by(username=form_username).first()

        if check_user:
            return redirect(url_for("signup"))

        else:
            new_user = User(
                firstname=form_firstname,
                lastname=form_lastname,
                username=form_username,
                password=form_password,
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect("/")
            except:
                return "There was an issue adding a new user."

    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(port=3000)
