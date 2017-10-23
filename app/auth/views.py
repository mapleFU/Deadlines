from . import auth_blueprint
# 用CURRENT_APP解决日志问题
from flask import render_template, url_for, flash, redirect, current_app
from .forms import LoginForm, RegistionForm
from ..model import User
from flask_login import login_user, logout_user, login_required, current_user
# 导入app.init 的 db
from .. import db


# 注意注明表单名称
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # .data 表示正确的信息
        email = login_form.email.data

        user = User.query.filter_by(email=email).first()
        current_app.logger.debug('email is {}, current user is {}'.format(
            email,
            user
        ))
        if user is not None:
            if user.verify_password(login_form.password.data):
                login_user(user, login_form.remember_me.data)
                # 返回URL而并非视图
                return redirect(url_for('main.index'))
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
        user = User.query.filter_by(email=register_form.email).first()
        if user is not None:
            flash('Email have been registed.')
        else:

            # .data is essential
            new_user = User(
                email=register_form.email.data,
                username=register_form.username.data,
                password=register_form.password1.data,
                        )
            current_app.logger.debug('create user : {}'.format(new_user))
            db.session.add(new_user)
            # TODO:do I really need commit it here?
            db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=register_form)


@login_required
@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return url_for('main.index')
