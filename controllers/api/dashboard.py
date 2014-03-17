#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin

from settings import MONGO_URI
from .base import get, post, put, delete


ADMIN_BUCKET_NAME = 'openminig-admin'
collection = 'dashboard'

dashboard_app = Bottle()
mongo = MongoPlugin(uri=MONGO_URI, db=ADMIN_BUCKET_NAME, json_mongo=True)
dashboard_app.install(mongo)


@dashboard_app.route('/', method='GET')
@dashboard_app.route('/<slug>', method='GET')
def dashboard_get(mongodb, slug=None):
    return get(mongodb, collection, slug)


@dashboard_app.route('/', method='POST')
def dashboard_post(mongodb, slug=None):
    return post(mongodb, collection)


@dashboard_app.route('/<slug>', method='PUT')
def dashboard_put(mongodb, slug=None):
    return put(mongodb, collection, slug)


@dashboard_app.route('/<slug>', method='DELETE')
def dashboard_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
