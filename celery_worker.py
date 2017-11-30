import os
from app import create_app, celery

import app.main.task_queue

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()
