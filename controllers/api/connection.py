#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin

from .base import api_get, api_post, api_put, api_delete


ADMIN_BUCKET_NAME = 'openminig-admin'

connection_app = Bottle()
mongo = MongoPlugin(uri="mongodb://127.0.0.1", db=ADMIN_BUCKET_NAME,
                    json_mongo=True)
connection_app.install(mongo)


@connection_app.route('/', method='GET')
@connection_app.route('/:slug', method='GET')
def connection_get(mongodb, slug=None):
    return api_get(mongodb, 'connection', slug)


@connection_app.route('/', method='POST')
def connection_post(mongodb, slug=None):
    return api_post(mongodb, 'connection')


@connection_app.route('/:slug', method='PUT')
def connection_put(mongodb, slug=None):
    return api_put(mongodb, 'connection', slug)


@connection_app.route('/:slug', method='DELETE')
def connection_delete(mongodb, slug=None):
    return api_delete(mongodb, 'connection', slug)
