import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config_class, Config
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_caching import Cache

from celery import Celery


bootstrap = Bootstrap()

db = SQLAlchemy()

images = UploadSet('images', IMAGES, default_dest=os.path.abspath('./static/icon/'))

cache = Cache(config={'CACHE_TYPE': 'simple'})

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def create_app(config_name):
    app = Flask(__name__)
    # 从instance中配置
    app.config.from_pyfile('../instance/config.py')
    # from object? no! from class!
    app.config.from_object(config_class[config_name])
    config_class[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    configure_uploads(app, images)
    # 限制大小
    patch_request_class(app)

    cache.init_app(app)

    # # 配置 celery 与别的结合
    # app.config.update(
    #     CELERY_BROKER_URL=' amqp://localhost',
    #     # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # )
    # celery = make_celery(app)
    app.config.update(celery.conf)

    from app.model import User

    # register blue print
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # 日志设定
    app.logger.setLevel('DEBUG')

    # app.logger.debug(config_name)

    # 把这个放到了最后
    # TODO: know how to adjust it
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    return app
