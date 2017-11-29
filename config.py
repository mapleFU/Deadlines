import os

basedir = os.path.abspath(os.path.abspath(__file__))
# TODO: find another way to do it
mysql_secret = os.environ.get('SQLCODE')


class Config:
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fuck you leather man'
    # 把COMMIT_ON_TEAR_DOWN 注释掉
    # COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEAR_DOWN = True
    # DATABASE_URI_FMT = 'mysql://root:{}@localhost:3306/deadblue'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue'.format(mysql_secret)
    FLASKY_ADMIN = os.environ.get('FLASK_ADMIN')
    UPLOADED_IMAGES_DEST = os.path.abspath('./app/static/icon/')
    UPLOADS_DEFAULT_DEST = os.path.abspath('./app/static/icon/')
    # UPLOADED_IMAGES_UPLOADS = './app/static/icon/'
    # UPLOAD_FOLDER = './app/static/icon'

    @staticmethod
    def init_app(app):
        # 用密码来更改
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI_FMT'].format(app.config['SQLCODE'])


class DevConfig(Config):
    DEBUG = True
    DATABASE_URI_FMT = 'mysql://root:{}@localhost:3306/deadblue_dev'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue_dev'.format(mysql_secret)
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEAR_DOWN = True


class ProductionConfig(Config):
    DATABASE_URI_FMT = 'mysql://root:{}@localhost:3306/deadblue'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue'.format(mysql_secret)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    DATABASE_URI_FMT = 'mysql://root:{}@localhost:3306/deadblue_test'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue_test'.format(mysql_secret)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# origin: config_class
config_class = {
    'dev': DevConfig,
    'product': ProductionConfig,
    'test': TestConfig,

    'default': DevConfig,
}
