#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from bottle import response, request
from datetime import datetime
from mining.utils import slugfy, parse_dumps


def base():
    response.set_header('charset', 'utf-8')
    response.content_type = 'application/json'


def get(mongodb, collection, slug, field={'key': 'slug'}):
    base()
    if slug:
        data = mongodb[collection].find_one({field['key']: slug})
        if data:
            data.pop('_id', None)
        else:
            data = {}
        return json.dumps(data, default=parse_dumps)
    else:
        data = mongodb[collection].find()
        response = []
        for d in data:
            d.pop('_id', None)
            response.append(d)
    return json.dumps(response, default=parse_dumps)


def post(mongodb, collection, opt={}, field={'key': 'slug', 'value': 'name'}):
    base()
    data = request.json
    data[field['key']] = data[field['value']]
    if field.get('key', '') == 'slug':
        data[field['key']] = slugfy(data[field['value']])
    data = dict(data.items() + opt.items())
    get = mongodb[collection].find({field['key']: data[field['key']]})
    if get.count() == 0:
        mongodb[collection].insert(data)
        del data['_id']
        return json.dumps(data, default=parse_dumps)
    return {'status': 'error', 'message': 'Object exist, please send PUT!'}


def put(mongodb, collection, slug, opt={}, field={'key': 'slug'},
        request_json=request.json):
    base()
    data = request_json or request.json or {}
    data[field['key']] = slug
    data = dict(data.items() + opt.items())
    if 'lastupdate' in data and isinstance(data.get('lastupdate'),
                                           basestring):
        data['lastupdate'] = datetime.strptime(data.get('lastupdate'),
                                               '%Y-%m-%d %H:%M:%S')
    if 'start_process' in data and isinstance(data.get('start_process'),
                                              basestring):
        data['start_process'] = datetime.strptime(data.get('start_process'),
                                                  '%Y-%m-%d %H:%M:%S')
    get = mongodb[collection].find_one({field['key']: slug})
    if get:
        mongodb[collection].update({field['key']: slug}, {'$set': data})
        return json.dumps(data, default=parse_dumps)
    return {'status': 'error',
            'message': 'Object not exist, please send POST to create!'}


def delete(mongodb, collection, slug, field={"key": "slug"}):
    base()
    get = mongodb[collection].find_one({field['key']: slug})
    if get:
        mongodb[collection].remove({field['key']: slug})
        return {'status': 'success'}
    return {'status': 'error',
            'message': 'Object not exist, please send POST to create!'}
