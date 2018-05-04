# 可以考虑把generate_fake变成一个函数
from . import db, cache
from flask_login import UserMixin, AnonymousUserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_moment import datetime
from flask import current_app

from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired

from datetime import date
from enum import Enum


class Message(db.Model):
    """
    站内信
    """
    __tablename__ = 'messages'
    # 站内信发送者

    sender_id = db.Column(db.INTEGER, db.ForeignKey('users.id'), primary_key=True)
    receiver_id = db.Column(db.INTEGER, db.ForeignKey('users.id'), primary_key=True)
    sender = db.relationship('User', back_populates="sent_messages", foreign_keys=[sender_id])
    # 站内信接受者
    receiver = db.relationship('User', back_populates="recv_messages", foreign_keys=[receiver_id])
    content = db.Column(db.Text)
    sent = db.Column(db.DateTime(), default=datetime.utcnow)


class User(db.Model, UserMixin):
    """
    申请创建的用户对象，拥有创建-删改任务的职责
    可以拥有头像 需要登录
    """
    __tablename__ = 'users'

    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    id = db.Column(db.INTEGER, primary_key=True)

    password_hash = db.Column(db.String(128))
    # task_id = db.Column(db.INTEGER, db.ForeignKey('Deadlines.id'))
    tasks = db.relationship('Deadline', backref='author', lazy='joined')
    # task_id = db.relationship(db.Integer, db.ForeignKey('task.id'))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # 是否上传头像
    icon_uploaded = db.Column(db.Boolean(), default=False)
    # 头像的URL
    icon_url = db.Column(db.String(64))
    # 发送的站内信
    sent_messages = db.relationship('Message', back_populates='sender',
                                    order_by='Message.sent', foreign_keys=[Message.sender_id],)
    # 接受的站内信
    recv_messages = db.relationship('Message', back_populates='receiver',
                                    order_by='Message.sent', foreign_keys=[Message.receiver_id],)

    def __init__(self, username, password, email):
        self.email = email
        self.username = username
        self.password = password

    @property
    def password(self):
        raise AttributeError('Can not call password')

    @password.setter
    def password(self, password_value):
        # 用WERKZEUG生成密码
        self.password_hash = generate_password_hash(password_value)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def generate_token(self, expiration=600):
        s = TimedJSONWebSignatureSerializer(current_app.config['secret'], expires_in=expiration)
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_token(token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def generate_fake(count=100):
        """
        在开发和测试模式下使用
        利用forgery_py生成100条测试字段
        """
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            usr = User(
                email=forgery_py.internet.email_address(),
                username=forgery_py.internet.user_name(True),
                password=forgery_py.lorem_ipsum.word(),
            )
            db.session.add(usr)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class Teacher(db.Model):
    """
    学院的老师
    与COURSE可能是多对多关系(一般是一门课一老师)
    冗余存储？那是啥？
    """
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship("Course", back_populates="teachers")


class Course(db.Model):
    """
    需要进行的课程
    与老师可能有一对多的关系
    暂时没有有 "课时" 的属性，但是搜索出来是和他关联的
    实时"提供导入课程表"？
    历史信息用"老师名称"们来维护
    """
    __tablename__ = 'course'

    # 课程号（学校课号不可信...
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 学校课程号
    course_id = db.Column(db.Integer)
    # 课程名
    course_name = db.Column(db.String(128))
    # 老师，有可能有多张表...
    teachers = db.relationship("Teacher", back_populates="course")


class CommentOnCourse(db.Model):
    """
    对课程的评论
    打分(五星制) + 文本
    跟课程、用户是一对一的关系
    """
    __tablename__ = 'commentoncourse'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    stars = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, text=None, stars=None):
        self.text = text
        self.stars = stars


class Deadline(db.Model):
    """
    需要处理的deadline对象
    """
    __tablename__ = 'deadline'

    id = db.Column(db.INTEGER, primary_key=True)

    ending = db.Column(db.DateTime)
    # deadline的描述文本
    content = db.Column(db.Text)
    # 任务标签
    tag = db.Column(db.String(40), index=True, nullable=True)
    # not user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @staticmethod
    def add_task(content, ending, author, app):
        """
        :return:
        """
        with app.app_context():
            tsk = Deadline(content=content, ending=ending, author=author)
            db.session.add(tsk)
            db.session.commit()
            cache.delete('index_pag')

    # TODO: FINISH THIS AND TEST THIS
    def count_remains(self):
        """
        :return: 计算出endtime距离调用函数的时候相距的时间
        """
        return datetime.utcnow() - self.ending

    def __repr__(self):
        return '<deadline: User:{}, text:{}, end:{}>'.format(
            self.user_id,
            self.content[:10],
            self.ending
        )

    @staticmethod
    def date_range(start_date, end_date, increment, period):
        result = []
        nxt = start_date
        delta = relativedelta(**{period: increment})
        while nxt <= end_date:
            result.append(nxt)
            nxt += delta
        return result

    @staticmethod
    def generate_fake(count=100):
        """
        在开发和测试模式下使用
        利用forgery_py生成100条测试字段
        """
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        from dateutil.relativedelta import relativedelta
        user_num = User.query.count()
        seed()
        start_date = datetime.now()
        end_date = start_date + relativedelta(days=1)
        end_date = end_date.replace(hour=19, minute=0, second=0, microsecond=0)

        for i in range(count):
            u = User.query.offset(randint(0, user_num-1)).first()
            tsk = Deadline(
                content=forgery_py.lorem_ipsum.sentence(),
                author=u,
                ending=start_date
            )
            db.session.add(tsk)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        # print(datetime.now())
        # print(type(datetime.now()))


