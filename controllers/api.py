#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, response, request
from bottle.ext.mongo import MongoPlugin

from bson.json_util import dumps


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


def api_post(mongodb, collection, request):
    api_base()
    request.GET.items()
    return {}


@api_app.route('/')
def index():
    return 'OpenMining API!'


@api_app.route('/connection', method='GET')
@api_app.route('/connection/:slug', method='GET')
def connection_get(mongodb, slug=None):
    return api_get(mongodb, 'connection', slug)


@api_app.route('/connection', method='POST')
@api_app.route('/connection/:slug', method='POST')
def connection_post(mongodb, slug=None):
    return api_post(mongodb, 'connection', request)
