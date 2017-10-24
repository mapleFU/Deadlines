from . import main_blueprint
from flask import render_template, abort, redirect, url_for
from flask_login import login_required
from app.model import User, Task
from .forms import TaskForm
from .. import db


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
    # print('username: {}'.format(username))
    # print(User)
    usr = User.query.filter_by(username=username).first()
    if usr is None:
        # 搜索的用户不存在，触发404 ERROR
        abort(404)
    return render_template('user.html', user=usr)


@main_blueprint.route('/user/edit/<username>')
@login_required
def user_edit(username):
    return 'Hello, ' + username


@main_blueprint.route('/task/edit', methods=['GET', 'POST'])
@login_required
def task_edit():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            context=form.task_content.data,
            ending=form.ending_time.data
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.index'))
    # Todo Edit it for it self
    return render_template('auth/register.html', form=form)
