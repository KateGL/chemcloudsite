# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemcloud.settings')
app = Celery(
    'chemcloud',
    broker='amqp://guest:guest@localhost//',
    backend='amqp://guest:guest@localhost//',
    include=['chemcloud.tasks']
    )

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task(bind=True)
def add(self, x, y):
    #print celery.AsyncResult.task_id
    print('task add2')
    return x + y
