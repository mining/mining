#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, response, request
from bottle.ext.mongo import MongoPlugin

from bson.json_util import dumps

from utils import slugfy


ADMIN_BUCKET_NAME = 'openminig-admin'

api_app = Bottle()
mongo = MongoPlugin(uri="mongodb://127.0.0.1", db=ADMIN_BUCKET_NAME,
                    json_mongo=True)
api_app.install(mongo)


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


@api_app.route('/')
def index():
    return 'OpenMining API!'


@api_app.route('/connection', method='GET')
@api_app.route('/connection/:slug', method='GET')
def connection_get(mongodb, slug=None):
    return api_get(mongodb, 'connection', slug)


@api_app.route('/connection', method='POST')
def connection_post(mongodb, slug=None):
    return api_post(mongodb, 'connection')


@api_app.route('/connection/:slug', method='PUT')
def connection_put(mongodb, slug=None):
    return api_put(mongodb, 'connection', slug)
