#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin

from redis import Redis
from rq import Queue

from utils import conf, parse_dumps
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
    cubes = list(mongodb[collection].find({'run': 'run'}, {'_id':False}))
    return json.dumps(cubes, default=parse_dumps)


@cube_app.route('/', method='POST')
def cube_post(mongodb, slug=None):
    ret = post(mongodb, collection, opt={'status': False})
    Queue(connection=Redis()).enqueue_call(
        func='bin.mining.run',
        args=(ret['slug'],),
        timeout=580
    )

    return ret


@cube_app.route('/<slug>', method='PUT')
def cube_put(mongodb, slug=None):
    ret = put(mongodb, collection, slug, opt={'status': False})
    Queue(connection=Redis()).enqueue_call(
        func='bin.mining.run',
        args=(ret['slug'],),
        timeout=580
    )

    return ret


@cube_app.route('/<slug>', method='DELETE')
def cube_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
