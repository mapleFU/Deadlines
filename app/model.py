from . import db
from flask_login import UserMixin, AnonymousUserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_moment import datetime


class User(db.Model, UserMixin):
    """
    申请创建的用户对象，拥有创建-删改任务的职责
    可以拥有头像 需要登录
    """
    __tablename__ = 'Users'

    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    id = db.Column(db.INTEGER, primary_key=True)

    password_hash = db.Column(db.String(128))
    # task_id = db.Column(db.INTEGER, db.ForeignKey('Tasks.id'))
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    # task_id = db.relationship(db.Integer, db.ForeignKey('task.id'))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, username, password, email):
        self.email = email
        self.username = username
        self.password = password

    # tasks = db.relationship(
    #     'tasks',
    #     backref='user',
    #     lazy='dynamic',
    # )

    @property
    def password(self):
        raise AttributeError('Can not call password')

    @password.setter
    def password(self, password_value):
        # 用WERKZEUG生成密码
        self.password_hash = generate_password_hash(password_value)

    def verify_password(self, password):
        print(password)
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


# class AnonymousUser(AnonymousUserMixin):
#     pass


class Task(db.Model):
    """
    需要处理的任务对象
    """
    __tablename__ = 'Tasks'

    id = db.Column(db.INTEGER, primary_key=True)

    ending = db.Column(db.DateTime)
    content = db.Column(db.Text)
    tag = db.Column(db.String(40), index=True) # 任务标签
    # not user
    # user = db.relationship('User', backref='tasks', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    # mother_fuck = db.Column(db.String(64))
    # lazy = 'dynamic', figure out why
    # 第一个表示User类的tablename -> user, 所以并非User

    # TODO: FINISH THIS
    def count_remains(self):
        """
        :return: 计算出endtime距离调用函数的时候相距的时间
        """
        pass

    def __repr__(self):
        return '<task: User:{}, text:{}, end:{}>'.format(
            self.user_id,
            self.content[:10],
            self.ending
        )




