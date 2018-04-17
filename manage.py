#!/usr/bin/env python
import os

from app import create_app, db
from app.model import User, Task
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask_moment import Moment
from flask_restful import Api
from app.celery_cfg import make_celery
# from flask_admin import Admin


app = create_app(os.getenv('FLASK_CONFIG') or 'dev')


manager = Manager(app)
migrate = Migrate(app, db)
migrate.init_app(app, db)
moment = Moment(app)


# admin = Admin(app, name='dead_list', template_mode='bootstrap3')


def make_shell_context():
    return dict(app=app, db=db, User=User, Task=Task)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
