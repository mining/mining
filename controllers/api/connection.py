#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin

from .base import get, post, put, delete


ADMIN_BUCKET_NAME = 'openminig-admin'
collection = 'connection'

connection_app = Bottle()
mongo = MongoPlugin(uri="mongodb://127.0.0.1", db=ADMIN_BUCKET_NAME,
                    json_mongo=True)
connection_app.install(mongo)


@connection_app.route('/', method='GET')
@connection_app.route('/:slug', method='GET')
def connection_get(mongodb, slug=None):
    return get(mongodb, collection, slug)


@connection_app.route('/', method='POST')
def connection_post(mongodb, slug=None):
    return post(mongodb, collection)


@connection_app.route('/:slug', method='PUT')
def connection_put(mongodb, slug=None):
    return put(mongodb, collection, slug)


@connection_app.route('/:slug', method='DELETE')
def connection_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
