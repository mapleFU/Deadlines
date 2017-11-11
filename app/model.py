# 可以考虑把generate_fake变成一个函数
from . import db
from flask_login import UserMixin, AnonymousUserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_moment import datetime
from datetime import date


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
    # task_id = db.Column(db.INTEGER, db.ForeignKey('Tasks.id'))
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    # task_id = db.relationship(db.Integer, db.ForeignKey('task.id'))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # 是否上传头像
    icon_uploaded = db.Column(db.Boolean(), default=False)
    # 发送的站内信
    sent_messages = db.relationship('Message', back_populates='sender',
                                    order_by='Message.sent', foreign_keys=[Message.sender_id],
                                    lazy='dynamic')
    # 接受的站内信
    recv_messages = db.relationship('Message', back_populates='receiver',
                                    order_by='Message.sent', foreign_keys=[Message.receiver_id],
                                    lazy='dynamic')

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
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

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


class Task(db.Model):
    """
    需要处理的任务对象
    """
    __tablename__ = 'tasks'

    id = db.Column(db.INTEGER, primary_key=True)

    ending = db.Column(db.DateTime)
    content = db.Column(db.Text)
    tag = db.Column(db.String(40), index=True) # 任务标签
    # not user
    # user = db.relationship('User', backref='tasks', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # mother_fuck = db.Column(db.String(64))
    # lazy = 'dynamic', figure out why
    # 第一个表示User类的tablename -> user, 所以并非User

    # TODO: FINISH THIS AND TEST THIS
    def count_remains(self):
        """
        :return: 计算出endtime距离调用函数的时候相距的时间
        """
        return datetime.utcnow() - self.ending

    def __repr__(self):
        return '<task: User:{}, text:{}, end:{}>'.format(
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
            tsk = Task(
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


