#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from bottle import Bottle, request
from bottle.ext.mongo import MongoPlugin
import datetime

from mining.utils import conf, parse_dumps
from .base import get, post, put, delete, base


collection = 'filter'

filter_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
filter_app.install(mongo)


@filter_app.route('/', method='GET')
@filter_app.route('/<slug>', method='GET')
def filter_get(mongodb, slug=None):
    return get(mongodb, collection, slug)


@filter_app.route('/', method='POST')
def filter_post(mongodb, slug=None):
    return post(mongodb, collection)


@filter_app.route('/<slug>', method='PUT')
def filter_put(mongodb, slug=None):
    base()
    data = request.json or {}
    data['slug'] = slug
    data = dict(data.items())
    if 'lastupdate' in data and isinstance(data.get('lastupdate'), basestring):
        data['lastupdate'] = datetime.strptime(data.get('lastupdate'),
                                               '%Y-%m-%d %H:%M:%S')
    if 'start_process' in data and isinstance(data.get('start_process'),
                                              basestring):
        data['start_process'] = datetime.strptime(data.get('start_process'),
                                                  '%Y-%m-%d %H:%M:%S')
    get = mongodb[collection].find_one({'slug': slug})
    if get:
        mongodb[collection].update({'slug': slug}, data)
        return json.dumps(data, default=parse_dumps)
    return {'status': 'error',
            'message': 'Object not exist, please send POST to create!'}


@filter_app.route('/<slug>', method='DELETE')
def filter_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
