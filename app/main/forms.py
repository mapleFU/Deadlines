from flask_wtf import FlaskForm
from wtforms import DateField, TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, Regexp
from wtforms.fields.html5 import DateTimeField, DateField


class TaskForm(FlaskForm):
    task_content = TextAreaField('Input what kind of deadline you are facing.', validators=[DataRequired()])
    ending_time = DateField('Deadline-time')

    submit = SubmitField('Submit')


class ProfileEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$',
        0,
        'User name must have only one letters, dots or underscores'
    )])

    submit = SubmitField('Submit')