#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import time
import schedule

from bottle.ext.mongo import MongoPlugin

from settings import ADMIN_BUCKET_NAME, MONGO_URI
from bin.mining import run


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


mongo = MongoPlugin(uri=MONGO_URI, db=ADMIN_BUCKET_NAME,
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
