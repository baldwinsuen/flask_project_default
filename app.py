# pylint: disable=no-member

from flask import Flask, redirect, url_for, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_login import login_user, login_required, logout_user, current_user

from datetime import datetime, date

from forms import LoginForm, RegisterForm, AddTaskForm, UpdateTaskForm
from models import db, User, Todo, login_manager

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

    task_owner = current_user.username
    tasks = Todo.query.filter(Todo.owner == task_owner).all()
    return render_template("todo.html", tasks=tasks)


@app.route("/todo/delete/<int:id>")
@login_required
def delete(id):
    delete_task = Todo.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/todo")

    except:
        return "There was a problem deleting this task."


@app.route("/todo/update/<int:id>", methods=["POST", "GET"])
@login_required
def update(id):
    task = Todo.query.get_or_404(id)
    form = UpdateTaskForm()
    if form.validate_on_submit():
        task.content = form.description.data
        d_date = form.due_date.data

        # @TODO
        # add checkbox that will allow you to remove due date
        task_date = None
        if d_date:
            task.due_date = d_date

        try:
            db.session.commit()
            return redirect("/todo")
        except:
            return "Your task could not be updated."

    else:

        return render_template("update.html", task=task, form=form)


@app.route("/todo/completed/<int:id>", methods=["POST", "GET"])
@login_required
def completed(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        completion = not task.completed
        task.completed = completion
        try:
            db.session.commit()
            return redirect("/todo")

        except:
            return "Task completion status could not be changed."

    return render_template("todo.html", task=task)


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
                return redirect("/todo")
    else:
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
        try:
            db.session.add(new_user)
            db.session.commit()
            return render_template("index.html")
        except:
            return "New user could not be added."

    else:
        return render_template("signup.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/addtask", methods=["POST", "GET"])
@login_required
def addtask():
    form = AddTaskForm()
    task_owner = current_user.username

    if form.validate_on_submit():
        task_description = form.description.data
        task_due_date = form.due_date.data
        new_task = Todo(
            content=task_description,
            due_date=task_due_date,
            owner=task_owner,
            completed=False,
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect("/todo")

    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(port=3000)
