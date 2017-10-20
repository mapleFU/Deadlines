from . import db
from flask_login import UserMixin, AnonymousUserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """
    申请创建的用户对象，拥有创建-删改任务的职责
    可以拥有头像 需要登录
    """
    __tablename__ = 'user'

    username = db.Column(db.String(64), unique=True, index=True)
    id = db.Column(db.INTEGER, primary_key=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Can not call password')

    @password.setter
    def password(self, password_value):
        # 用WERKZEUG生成密码
        self.password_hash = generate_password_hash(password_value)

    def verify_password(self, password):
        raise check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(
            self.username
        )


class AnonymousUser(AnonymousUserMixin):
    pass


class Tasks(db.Model):
    """
    需要处理的任务对象
    """
    __tablename__ = 'tasks'

    id = db.Column(db.INTEGER, primary_key=True)
    endtime = db.Column(db.DateTime)
    context = db.Column(db.Text)
    users = db.relationship('User', backref='task')

