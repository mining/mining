# -*- coding: utf-8 -*-
from os import sys, path
import schedule
from time import sleep

from bottle.ext.mongo import MongoPlugin

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from mining.utils import conf, log_it
from mining.tasks import process


log_it("START", "bin-scheduler")
onrun = {}
register = []


def job(cube):
    log_it("START JOB: {}".format(cube.get('slug')), "bin-scheduler")
    process.delay(cube)
    log_it("END JOB: {}".format(cube.get('slug')), "bin-scheduler")


def rules(cube, scheduler_type='minutes', scheduler_interval=59,
          dashboard=None):
    if scheduler_type:
        scheduler_type = cube.get('scheduler_type', 'minutes')
    if scheduler_interval:
        scheduler_interval = cube.get('scheduler_interval', 59)

    log_it("START REGISTER", "bin-scheduler")
    log_it("cube: {}".format(cube.get('slug')), "bin-scheduler")
    log_it("type: {}".format(scheduler_type), "bin-scheduler")
    log_it("interval: {}".format(scheduler_interval), "bin-scheduler")
    log_it("END REGISTER", "bin-scheduler")

    t = {}
    if scheduler_type == 'minutes':
        env = schedule.every(int(scheduler_interval))
        t = env.minutes
    elif scheduler_type == 'hour':
        env = schedule.every()
        t = env.hour
    elif scheduler_type == 'day':
        env = schedule.every()
        t = env.day
    else:
        return False

    jobn = cube.get("slug")
    try:
        t.do(job, cube=cube)
        if dashboard:
            jobn = u"{}-{}".format(cube.get("slug"), dashboard)
        onrun[jobn] = env
        register.append(jobn)
        if cube.get('run') != 'run':
            process.delay(cube)
    except Exception, e:
        if jobn in register:
            register.remove(jobn)
        if onrun.get(jobn):
            del onrun[jobn]
        log_it("ERROR {}: {}".format(cube.get('slug'), e))

    return True


def scheduler_app():
    mongo = MongoPlugin(
        uri=conf("mongodb")["uri"],
        db=conf("mongodb")["db"],
        json_mongo=True).get_mongo()

    for cube in mongo['cube'].find({'scheduler_status': True}):
        rules(cube)

    for dashboard in mongo['dashboard'].find({'scheduler_status': True}):
        elements = [e['id'] for e in dashboard['element']]
        for e in elements:
            element = mongo['element'].find_one({'slug': e})
            cube = mongo['cube'].find_one({'slug': element['cube']})
            rules(cube, dashboard['scheduler_type'],
                  dashboard['scheduler_interval'])

    while True:
        for cube in mongo['cube'].find({'scheduler_status': True}):
            if cube['slug'] not in register:
                rules(cube)

        for dashboard in mongo['dashboard'].find({'scheduler_status': True}):
            elements = [e['id'] for e in dashboard['element']]
            for e in elements:
                element = mongo['element'].find_one({'slug': e})
                cube = mongo['cube'].find_one({'slug': element['cube']})
                if cube['slug'] not in register:
                    rules(cube, dashboard['scheduler_type'],
                          dashboard['scheduler_interval'],
                          dashboard['slug'])

        for cube in mongo['cube'].find({'scheduler_status': False}):
            if cube['slug'] in register:
                schedule.cancel_job(onrun[cube['slug']])
                del onrun[cube['slug']]
                register.remove(cube['slug'])

        for dashboard in mongo['dashboard'].find({'scheduler_status': False}):
            elements = [e['id'] for e in dashboard['element']]
            for e in elements:
                try:
                    element = mongo['element'].find_one({'slug': e})
                    cube = mongo['cube'].find_one({'slug': element['cube']})
                    jobn = u"{}-{}".format(cube['slug'], dashboard['slug'])
                    if jobn in register:
                        schedule.cancel_job(onrun[jobn])
                        del onrun[jobn]
                        register.remove(jobn)
                except:
                    pass

        schedule.run_pending()
        sleep(1)
