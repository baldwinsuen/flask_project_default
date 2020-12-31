from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, Length, Optional
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired(), Length(min=4, max=15)]
    )

    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=8, max=80)]
    )

    remember = BooleanField("remember me")


class RegisterForm(FlaskForm):
    email = StringField(
        "email",
        validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)],
    )
    username = StringField(
        "username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=8, max=80)]
    )


class AddTaskForm(FlaskForm):
    description = StringField(u"Description", widget=TextArea())

    due_date = DateField("Due Date", format="%Y-%m-%d", validators=[Optional()])


class UpdateTaskForm(FlaskForm):
    description = StringField(u"Description", widget=TextArea())

    due_date = DateField("Due Date", format="%Y-%m-%d", validators=[Optional()])
