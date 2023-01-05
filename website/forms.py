from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, URL, Length, Email
from flask_ckeditor import CKEditorField



class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "email@email.com"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5)], render_kw={"placeholder": "password"})
    confirm_password = PasswordField("confirm password", validators=[DataRequired(), Length(min=5)], render_kw={"placeholder": "password"})
    number = StringField("Phone number", validators=[DataRequired(), Length(min=9, max=9)], render_kw={"placeholder": "Enter in 9-digit format"})
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "email@email.com"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "password"})
    submit = SubmitField("Log in")
