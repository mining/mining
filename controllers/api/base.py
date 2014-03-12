#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import response, request

from bson.json_util import dumps

from utils import slugfy


def base():
    response.set_header('charset', 'utf-8')
    response.content_type = 'application/json'


def get(mongodb, collection, slug):
    base()
    if slug:
        return dumps(mongodb[collection].find({'slug': slug}))
    return dumps(mongodb[collection].find())


def post(mongodb, collection):
    base()
    data = request.json
    data['slug'] = slugfy(data['name'])
    get = mongodb[collection].find({'slug': data['slug']})
    if get.count() == 0:
        mongodb[collection].insert(data)
        return {'status': 'success', 'data': data}
    return {'status': 'error', 'message': 'Object exist, please send PUT!'}


def put(mongodb, collection, slug):
    base()
    data = request.json
    data['slug'] = slug
    get = mongodb[collection].find_one({'slug': slug})
    if get:
        mongodb[collection].update({'slug': slug}, data)
        return {'status': 'success', 'data': data}
    return {'status': 'error',
            'message': 'Object not exist, please send POST to create!'}


def delete(mongodb, collection, slug):
    base()
    mongodb[collection].remove({'slug': slug})
    return {'status': 'success'}
