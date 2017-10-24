from flask_wtf import FlaskForm
from wtforms import DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    task_content = TextAreaField('Input what kind of deadline you are facing.', validators=[DataRequired()])
    ending_time = DateField('Deadline-time', validators=[DataRequired()], format='%Y-%m-%d')

    submit = SubmitField('Submit')
