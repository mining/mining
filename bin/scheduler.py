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
from utils import conf, log_it


log_it("START", "bin-scheduler")


def job(slug):
    log_it("RUN JOB: {}".format(slug), "bin-scheduler")
    run(slug)


def rules(cube):
    scheduler_type = cube.get('scheduler_type', 'minutes')
    scheduler_interval = int(cube.get('scheduler_interval', 60))

    log_it("START REGISTER", "bin-scheduler")
    log_it("cube: {}".format(cube.get('slug')), "bin-scheduler")
    log_it("type: {}".format(scheduler_type), "bin-scheduler")
    log_it("interval: {}".format(scheduler_interval), "bin-scheduler")
    log_it("END REGISTER", "bin-scheduler")

    t = {}
    if scheduler_type == 'minutes':
        t = schedule.every(scheduler_interval).minutes
    elif scheduler_type == 'hour':
        t = schedule.every().hour
    elif scheduler_type == 'day':
        t = schedule.every().day

    try:
        t.do(job, slug=cube.get('slug'))
    except Exception, e:
        log_it("ERROR {}: {}".format(cube.get('slug'), e))


mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True).get_mongo()

register = []
for cube in mongo['cube'].find({'scheduler_status': True}):
    rules(cube)
    register.append(cube['slug'])


while True:
    for cube in mongo['cube'].find({'scheduler_status': True}):
        if cube['slug'] not in register:
            rules(cube)

    schedule.run_pending()
    time.sleep(1)
