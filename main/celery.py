import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings.settings')

app = Celery('main', backend='amqp',)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))

CELERY_TIMEZONE = 'UTC'


def get_celery_worker_status():
    """
    Returns celery status
    """
    ERROR_KEY = 'ERROR'
    try:
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if not d:
            d = {
                ERROR_KEY: 'No running Celery workers were found.'}
    except IOError as e:
        from errno import errorcode
        msg = 'Error connecting to the backend: ' + str(e)
        if len(e.args) > 0 and errorcode.get(e.args[0]) == 'ECONNREFUSED':
            msg += ' Check that the Redis server is running.'
        d = {
            ERROR_KEY: msg}
    except ImportError as e:
        d = {
            ERROR_KEY: str(e)}
    return d
