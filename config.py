import os
from random import randint

basedir = os.path.abspath(os.path.abspath(__file__))
# TODO: find another way to do it
mysql_secret = os.environ.get('SQLCODE')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fuck you leather man'
    # COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEAR_DOWN = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue'.format(mysql_secret)

    FLASKY_ADMIN = os.environ.get('FLASK_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_BASE_URL') or \
    #                           "sqlite:///" + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue_dev'.format(mysql_secret)
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEAR_DOWN = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue'.format(mysql_secret)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue_test'.format(mysql_secret)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# origin: config_class
config_class = {
    'dev': DevConfig,
    'product': ProductionConfig,
    'test': TestConfig,

    'default': DevConfig,
}
