from . import main_blueprint
from flask import render_template, abort, redirect, url_for, request
from flask_login import login_required, current_user
from app.model import User, Task
from .forms import TaskForm
from .. import db


@main_blueprint.route('/base')
def base2():
    return render_template('base.html')


@main_blueprint.route('/', methods=['GET', 'POST'])
@main_blueprint.route('/DeadBlue', methods=['GET', 'POST'])
@main_blueprint.route('/deadblue', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if current_user.is_authenticated and form.validate_on_submit():
        tsk = Task(
            content=form.task_content.data,
            ending=form.ending_time.data,
            author=current_user
        )

        db.session.add(tsk)
        db.session.commit()
        # maybe i should clear it?
        return redirect(url_for('.index'))
    # attention
    page = request.args.get('page', 1, type=int)
    pag = Task.query.order_by(Task.ending).paginate(
        page, per_page=10, error_out=False
    )
    # tasks = Task.query.order_by(Task.ending).all()
    # print(tasks)
    tasks = pag.items
    return render_template('index.html', tsks=tasks, form=form)


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
