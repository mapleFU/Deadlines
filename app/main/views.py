import os

from . import main_blueprint
from flask import render_template, abort, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.model import User, Task
from .forms import images, IconForm, TaskForm, PasswordEditForm, ProfileEditForm
from .. import db, cache
from sqlalchemy.orm import joinedload, loading

from .task_queue import remove_icon

@main_blueprint.route('/base')
def base2():
    return render_template('base.html')


GET_INDEX_PAG = 'get_index_pag'


@cache.memoize(100)
def get_index_pag(page):
    """
    :param page: 页面的目录数
    :return: 对应的缓存
    注意，数据库查询不应该用缓存
    """

    return db.session.query(Task).option(joinedload(Task.author)).order_by(Task.ending).paginate(
        page, per_page=10, error_out=False
    ).items


@cache.cached(timeout=100, key_prefix='get_first_pag')
def get_first_pag():
    """
    :param page: 查询的页面数
    :return:    返回查询的页面
    """
    pg1 = db.session.query(Task).order_by(Task.ending).paginate(
        1, per_page=10, error_out=False
    ).items
    # record
    # q_tsk = db.session.query(Task)
    # q_tsk.merge_result(pg1)
    q_usr = db.session.query(User)
    # FIX IT, 得出的查询的对象需要绑定到缺失对象的 SESSION（对应的QUERY上）
    q_usr.merge_result(tsk.author for tsk in pg1)
    # db.session.query.merge_result()
    # current_app.logger.debug(type(rt1), rt1)
    return pg1


@main_blueprint.route('/', methods=['GET', 'POST'])
@main_blueprint.route('/DeadBlue', methods=['GET', 'POST'])
@main_blueprint.route('/deadblue', methods=['GET', 'POST'])
def index():
    current_app.logger.debug(current_app.config['SQLALCHEMY_DATABASE_URI'])
    form = TaskForm()
    if current_user.is_authenticated and form.validate_on_submit():
        # 把TASK更新抽象出来，封装成一个函数，触发这个函数会删除cache
        Task.add_task(content=form.task_content.data, ending=form.ending_time.data,
                      author=current_user, app=current_app)
        # tsk = Task(
        #     content=form.task_content.data,
        #     ending=form.ending_time.data,
        #     author=current_user
        # )
        #
        # db.session.add(tsk)
        # db.session.commit()
        # cache.delete_memoized('get_index_pag')
        # maybe i should clear it?
        return redirect(url_for('.index'))
    # attention 这里应该使用缓存
    page = request.args.get('page', 1, type=int)
    # paginate 分页
    if page == 1:
        pag = get_first_pag()
    else:
        pag = get_index_pag(page)
    tasks = pag
    # author = pag[0].author
    # print('fuck you {}'.format(author))
    # TODO:搞清楚tmd 缓存关系
    # print(tasks)
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


@main_blueprint.route('/user/edit/<username>', methods=['GET', 'POST'])
@login_required
def user_edit(username):
    if current_user.username != username:
        abort(403)
    edit_form = ProfileEditForm()
    pwd_form = PasswordEditForm()
    icon_form = IconForm()

    # 为什么要两个.. 为了USER?

    # 这个URL 是相对在页面上的 URL
    BASE_URL = '/static/icon/'
    # file_url = '../../static/icon/base.png'
    if current_user.icon_uploaded:
        # 已经上传头像
        file_url = current_user.icon_url
    else:
        file_url = '/static/icon/base.png'

    if edit_form.validate_on_submit() and edit_form.submit.data:

        # usr is already current user
        new_username = edit_form.username.data
        usr = User.query.filter_by(username=new_username).first()
        if usr is not None:
            if usr is current_user:
                flash('You didn\'t change it')
            else:
                flash('User with name {wanna_set} already existed.'.format(wanna_set=edit_form.username.data))
        else:
            username = edit_form.username.data
            # usr.username = username
            current_user.username = username
            db.session.add(current_user)
            db.session.commit()
        # url may changed, directed.
        return redirect(url_for('.user_edit', username=username))
    elif pwd_form.validate_on_submit() and pwd_form.submit.data:
        if current_user.verify_password(pwd_form.origin_pwd.data):
            # 密码验证成功
            current_user.password = pwd_form.new_pwd1.data
            db.session.add(current_user)
            db.session.commit()
        else:
            flash('Password Error When Editing Password')
        return redirect(url_for('.user_edit', username=username))
    elif icon_form.validate_on_submit() and icon_form.submit.data:
        # current_app.logger.debug(current_user.id)

        # , name=str(current_user.id), 似乎是类型指定有误
        # current_app.logger.debug(images)
        # current_app.logger.debug(images.default_dest)
        # current_app.logger.debug('BASE: ' + os.path.abspath(BASE_URL))
        # current_app.logger.debug('DEFAULT: ' + os.path.abspath(images.default_dest))

        # 主要有文件名后缀的问题和folder对应URL的问题, 我日，不是？
        filename = images.save(icon_form.icon.data, name=icon_form.icon.data.filename)

        # 把旧的放进队列, 等待删除
        try:
            app_url = current_app.config['UPLOADED_IMAGES_DEST'] + '/' + current_user.icon_url.lstrip(BASE_URL)
            print('remove' + app_url)
            remove_icon.delay(app_url)
            # os.remove(app_url)
        except FileNotFoundError:
            print('heyhey')

        file_url = BASE_URL + filename
        # TODO: figure how does file exists and how to delete it
        if current_user.icon_uploaded:
            old_icon = current_user.icon_url
        current_user.icon_uploaded = True
        current_user.icon_url = file_url
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('.user_edit', username=username))

    edit_form.username.data = username
    # TODO: fix it
    # print(file_url)
    # current_app.logger.debug('FINAL: ' + file_url)
    return render_template('edit_user.html', form_tuple=(edit_form, pwd_form, icon_form), file_url=file_url)


@main_blueprint.route('/task/edit', methods=['GET', 'POST'])
@login_required
def task_edit():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            content=form.task_content.data,
            ending=form.ending_time.data,
            author=current_user
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.index'))
    # Todo Edit it for it self
    return render_template('auth/register.html', form=form)
