# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import Celery

app = Celery(
    'proj',
    backend='amqp://',
    broker='amqp://',
    include=['proj.tasks'],
)
app.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_TASK_SERIALIZER='json',
)

if __name__ == '__main__':
    app.start()
