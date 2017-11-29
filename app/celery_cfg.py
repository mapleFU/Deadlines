from celery import Celery, Task


def make_celery(app):
    print(app.config)
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery
