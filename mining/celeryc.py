# -*- coding: utf-8 -*-
from celery import Celery

from mining.utils import conf


celery_app = Celery(
    'mining.tasks',
    broker=conf("celery").get("broker", 'amqp://'),
    backend=conf("celery").get("backend", 'amqp://'),
    include=['mining.tasks'])

celery_app.conf.update(**conf("celery").get("params", {}))
