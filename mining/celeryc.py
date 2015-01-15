# -*- coding: utf-8 -*-
from celery import Celery

from mining.utils import conf


celery_app = Celery(
    'mining.tasks',
    broker=conf("celery").get("broker", 'amqp://'),
    backend=conf("celery").get("backend", 'amqp://'),
    include=['mining.tasks'])

celery_app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=conf("celery").get("result_expires", 3600),
    CELERYD_POOL="gevent"
)
