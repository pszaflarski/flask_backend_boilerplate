from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, DataRequired, EqualTo


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class PasswordForm(Form):
    password = PasswordField('Password', validators=[
        DataRequired(),
    ])
    confirm = PasswordField('Confirm Password', validators=[
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Submit')


class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Submit')


class NewUserForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[
        DataRequired(),
    ])
    confirm = PasswordField('Confirm Password', validators=[
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Submit')
