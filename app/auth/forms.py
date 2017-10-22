from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..model import User


class LoginForm(FlaskForm):
    """
    登陆的表单，需要输入email和password字段
    """
    email = StringField('You email', validators=[Email(), Length(1, 64), DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Length(1, 64)])
    remember_me = BooleanField('remember me', default=False)
    submit = SubmitField('log in')


class RegistionForm(FlaskForm):
    """
    注册表单，需要EMAIL 用户名并且填写两次password
    """
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    username = StringField('Username', validators=[DataRequired(), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$',
        0,
        'User name must have only one letters, dots or underscores'
    )])

    password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    submit = SubmitField('Register')

    # 我也不晓得为啥要两个参数
    # def validate_username(self, username):
    #     if User.query.filter_by(username=username).first() is None:
    #         raise ValidationError('The username have been used!')
    #
    # def validate_email(self, email):
    #     if User.query.filter_by(email=email).first() is None:
    #         raise ValidationError('The email have been used!')

    # 抛出的异常会显示，这里会在表单提交的时候被调用
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError('The username have been used!')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError('The email have been used!')
