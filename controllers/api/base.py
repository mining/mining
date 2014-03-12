#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import response, request

from bson.json_util import dumps

from utils import slugfy


def api_base():
    response.set_header('charset', 'utf-8')
    response.content_type = 'application/json'


def api_get(mongodb, collection, slug):
    api_base()
    if slug:
        return dumps(mongodb[collection].find({'slug': slug}))
    return dumps(mongodb[collection].find())


def api_post(mongodb, collection):
    api_base()
    data = request.json
    data['slug'] = slugfy(data['name'])
    get = mongodb[collection].find({'slug': data['slug']})
    if get.count() == 0:
        mongodb[collection].insert(data)
        return {'status': 'success', 'data': data}
    return {'status': 'error', 'message': 'Object exist, please send PUT!'}


def api_put(mongodb, collection, slug):
    api_base()
    data = request.json
    data['slug'] = slug
    get = mongodb[collection].find_one({'slug': slug})
    if get:
        mongodb[collection].update({'slug': slug}, data)
        return {'status': 'success', 'data': data}
    return {'status': 'error',
            'message': 'Object not exist, please send POST to create!'}


def api_delete(mongodb, collection, slug):
    api_base()
    mongodb[collection].remove({'slug': slug})
    return {'status': 'success'}
