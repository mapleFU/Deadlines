from . import auth_blueprint
from flask import render_template, url_for, flash
from .forms import LoginForm, RegistionForm
from ..model import User
from flask_login import login_user


# 注意注明表单名称
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # .data 表示正确的信息
        email = login_form.email.data
        current_user = User.query.filter_by(email=email).first()
        if current_user is not None:
            if current_user.verify_password(login_form.password):
                login_user(current_user, login_form.remember_me)
                # 返回URL而并非视图
                return url_for('main.index')
            else:
                flash('password error')
        else:
            flash('Email not exist!')
    # 弄清楚那这里为啥不返回视图
    return render_template('auth/login.html', form=login_form)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册所用视图函数
    """
    register_form = RegistionForm()
    if register_form.validate_on_submit():
        pass