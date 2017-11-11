from flask_wtf import FlaskForm
from wtforms import DateField, TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Regexp, Length, EqualTo
from wtforms.fields.html5 import DateTimeField, DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES


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

    submit = SubmitField('Update username')


class PasswordEditForm(FlaskForm):
    """
    编辑密码的表单
    TODO:最好确定以下表单是否需要添加别的非表单(比如忘记密码)
    """
    PWD_VALIDATORS = [DataRequired(), Length(1, 64)]
    origin_pwd = PasswordField('Old Password', validators=PWD_VALIDATORS)
    new_pwd1 = PasswordField('New Password',
                             validators=[EqualTo('new_pwd2', 'Password must match')] + PWD_VALIDATORS)
    new_pwd2 = PasswordField('Confirm Password', validators=PWD_VALIDATORS)

    submit = SubmitField('Update Password')


images = UploadSet('images', IMAGES)


class IconForm(FlaskForm):
    icon = FileField('Your new icon', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only')
    ])
