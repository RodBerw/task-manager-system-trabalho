from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    assigned_user = SelectField('Assigned User', choices=[])
    submit = SubmitField('Create Task')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.assigned_user.choices = [(user.username, user.username) for user in User.query.all()]

class UpdateTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Doing', 'Doing'), ('Completed', 'Completed')])
    assigned_user = SelectField('Assigned User', choices=[])
    submit = SubmitField('Update Task')

    def __init__(self, *args, **kwargs):
        super(UpdateTaskForm, self).__init__(*args, **kwargs)
        self.assigned_user.choices = [(user.username, user.username) for user in User.query.all()]
    