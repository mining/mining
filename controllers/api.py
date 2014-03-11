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


def api_get(mongodb, collection, slug=None):
    return dumps(mongodb[collection].find())


@api_app.route('/')
def index():
    return 'OpenMining API!'


@api_app.route('/connection/')
def connection_get(mongodb):
    return api_get(mongodb, 'connection')
