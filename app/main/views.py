from . import main_blueprint
from flask import render_template, abort
from flask_login import login_required
from app.model import User


@main_blueprint.route('/base')
def base2():
    return render_template('base.html')


@main_blueprint.route('/')
@main_blueprint.route('/DeadBlue')
@main_blueprint.route('/deadblue')
def index():
    return render_template('index.html')


@main_blueprint.route('/task')
@login_required
def task():
    """
    :return: DDL 任务页面
    """
    return render_template('tasks.html')


@main_blueprint.route('/user/<username>')
@login_required
def user(username):
    """
    :return: 用户资料页面
    """
    usr = User.query.filter(username=username).first()
    if usr is None:
        # 搜索的用户不存在，触发404 ERROR
        abort(404)
    return render_template('user.html', user=usr)


@main_blueprint.route('/user/edit/<username>')
@login_required
def user_edit(username):
    pass


@main_blueprint.route('/task/edit')
@login_required
def task_edit():
    pass