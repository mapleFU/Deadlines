from . import mail_blueprint
# 用CURRENT_APP解决日志问题
from flask import render_template, url_for, flash, redirect, current_app
from .forms import LoginForm, RegistionForm
from ..model import User, Message
from flask_login import login_user, logout_user, login_required, current_user
# 导入app.init 的 db
from .. import db


@mail_blueprint.route('/')
@login_required
def mail():
    # 发送的邮件
    sendered = Message.query.filter_by(sender=current_user).all()
    # 接受的邮件
    received = Message.query.filter_by(receiver=current_user).all()


@mail_blueprint.route('/edit')
def edit_main():
    pass
