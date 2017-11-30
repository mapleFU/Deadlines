from celery import Celery


def make_celery(app):
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    app.config.update(celery.conf)
    return celery
