from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

# Add User
# Login
# Edit User


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class EditUserForm(FlaskForm):
    """Form for editing users."""

    username = StringField('(Optional) Username', validators=[DataRequired()])
    email = StringField('(Optional) E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('(Optional) Password', validators=[Length(min=6)])