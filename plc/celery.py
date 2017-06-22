from __future__ import absolute_import
import os
from celery import Celery
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plc.settings')
from django.conf import settings
app = Celery('plc', broker='redis://localhost')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERYBEAT_SCHEDULE = {
        # 'do-task-every-5-seconds': {
        #     'task': 'plcProject.tasks.read_data_fromplc',
        #     #'args': (2,3),
        #     'schedule': timedelta(seconds=5),
        # },
        'do-task-every-10-seconds':{
        	'task': 'plcProject.tasks.delloc_database',
        	'schedule': timedelta(seconds=10),
        }
    },
)
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))