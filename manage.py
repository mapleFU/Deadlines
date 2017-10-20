import os

from app import create_app, db
from flask_migrate import Migrate, MigrateCommand

app = create_app('dev')

migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    app.run()
