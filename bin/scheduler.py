#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

from os import sys, path
import time
import schedule

from bottle.ext.mongo import MongoPlugin

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from bin.mining import run
from utils import conf


def job(slug):
    run(slug)


def rules(cube):
    scheduler_type = cube.get('scheduler_type', 'minutes')
    scheduler_interval = cube.get('scheduler_interval', 60)

    if scheduler_type == 'minutes':
        t = schedule.every(int(scheduler_interval)).minutes
    elif scheduler_type == 'hour':
        t = schedule.every().hour
    elif scheduler_type == 'day':
        t = schedule.every().day
    else:
        return None
    t.do(job, slug=cube.get('slug'))


mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True).get_mongo()

register = []
for cube in mongo['cube'].find({'scheduler': True}):
    rules(cube)
    register.append(cube['slug'])


while True:
    for cube in mongo['cube'].find({'scheduler': True}):
        if cube['slug'] not in register:
            rules(cube)

    schedule.run_pending()
    time.sleep(1)
