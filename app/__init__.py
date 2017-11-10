from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config_class
from flask_login import LoginManager


bootstrap = Bootstrap()

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    # from object? no! from class!
    app.config.from_object(config_class[config_name])
    # 从instance中配置
    app.config.from_pyfile('../instance/config.py')

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from app.model import User

    # TODO: know how to adjust it
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()
    # register blue print
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.logger.setLevel('INFO')

    return app
