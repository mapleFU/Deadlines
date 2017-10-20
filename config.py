import os
from random import randint

basedir = os.path.abspath(os.path.abspath(__file__))
mysql_secret = os.environ.get('SQLCODE')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fuck you leather man'

    SQLALCHEMY_COMMIT_ON_TEAR_DOWN = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue'.format(mysql_secret)

    FLASKY_ADMIN = os.environ.get('FLASK_ADMIN')


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue_dev'.format(mysql_secret)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue'.format(mysql_secret)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:{}@localhost:3306/deadblue_test'.format(mysql_secret)


# origin: config_class
config_class = {
    'dev': DevConfig,
    'product': ProductionConfig,
    'test': TestConfig,

    'default': DevConfig,
}