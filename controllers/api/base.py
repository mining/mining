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
        data = mongodb[collection].find({'slug': slug})
    else:
        data = mongodb[collection].find()
    response = []
    for d in data:
        del d['_id']
        response.append(d)
    return dumps(response)


def post(mongodb, collection, opt={}, field={'key': 'slug', 'value': 'name'}):
    base()
    data = request.json
    data[field['key']] = slugfy(data[field['value']])
    data = dict(data.items() + opt.items())
    get = mongodb[collection].find({field['key']: data[field['key']]})
    if get.count() == 0:
        mongodb[collection].insert(data)
        del data['_id']
        return data
    return {'status': 'error', 'message': 'Object exist, please send PUT!'}


def put(mongodb, collection, slug, opt={}, field={'key': 'slug'},
        request_json=request.json):
    base()
    data = request_json
    data[field['key']] = slug
    data = dict(data.items() + opt.items())
    get = mongodb[collection].find_one({field['key']: slug})
    if get:
        mongodb[collection].update({field['key']: slug}, data)
        return data
    return {'status': 'error',
            'message': 'Object not exist, please send POST to create!'}


def delete(mongodb, collection, slug, field={"key": "slug"}):
    base()
    mongodb[collection].remove({'slug': slug})
    return {'status': 'success'}
