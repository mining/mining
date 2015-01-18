# -*- coding: utf-8 -*-
import json
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin
import datetime

from mining.utils import conf, parse_dumps
from mining.tasks import process
from .base import get, post, put, delete


collection = 'cube'

cube_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
cube_app.install(mongo)


@cube_app.route('/', method='GET')
@cube_app.route('/<slug>', method='GET')
def cube_get(mongodb, slug=None):
    return get(mongodb, collection, slug)


@cube_app.route('/runing-cubes', method='GET')
def cube_get_runing(mongodb, slug=None):
    cubes = list(mongodb[collection].find(
        {'run': 'run'}, {'_id': False}).sort([('last_update', -1)]))
    return json.dumps(cubes, default=parse_dumps)


@cube_app.route('/late-cubes', method='GET')
def cube_get_late(mongodb, slug=None):
    _cubes = list(mongodb[collection].find({}, {'_id': False}))
    cubes = []
    for cb in _cubes:
        is_late = False
        if cb.get('scheduler_type', '') == 'minutes':
            lu = cb.get('lastupdate')
            if isinstance(lu, datetime.datetime):
                n_lu = lu + datetime.timedelta(
                    minutes=int(cb['scheduler_interval']))
                if (datetime.datetime.now() - n_lu).total_seconds() > 0:
                    cb['late'] = n_lu
                    is_late = True
        elif cb.get('scheduler_type', '') == 'hour':
            pass
        elif cb.get('scheduler_type', '') == 'day':
            pass
        if is_late:
            cubes.append(cb)
    return json.dumps(cubes, default=parse_dumps)


@cube_app.route('/', method='POST')
def cube_post(mongodb, slug=None):
    ret = post(mongodb, collection, opt={'status': False})
    try:
        cube = json.loads(ret)
        process.delay(cube)
    except TypeError:
        pass

    return ret


@cube_app.route('/<slug>', method='PUT')
def cube_put(mongodb, slug=None):
    ret = put(mongodb, collection, slug, opt={'status': False})
    cube = json.loads(ret)
    process.delay(cube)
    return ret


@cube_app.route('/<slug>', method='DELETE')
def cube_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
