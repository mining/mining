#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from bottle import Bottle, request
from bottle.ext.mongo import MongoPlugin

from .base import get, post, put, delete

from element import collection as collection_element

ADMIN_BUCKET_NAME = 'openminig-admin'
collection = 'dashboard'

dashboard_app = Bottle()
mongo = MongoPlugin(uri="mongodb://127.0.0.1", db=ADMIN_BUCKET_NAME,
                    json_mongo=True)
dashboard_app.install(mongo)


@dashboard_app.route('/', method='GET')
@dashboard_app.route('/<slug>', method='GET')
def dashboard_get(mongodb, slug=None):
    da = get(mongodb, collection, slug)
    if 'full' not in request.GET:
        return da
    response = json.loads(da)[0]
    elements = response['element']
    response['element'] = []
    for el in elements:
        n_el = mongodb[collection_element].find_one({'slug': el})
        if n_el:
            del n_el['_id']
            response['element'].append(n_el)
    return response



@dashboard_app.route('/', method='POST')
def dashboard_post(mongodb, slug=None):
    return post(mongodb, collection)


@dashboard_app.route('/<slug>', method='PUT')
def dashboard_put(mongodb, slug=None):
    return put(mongodb, collection, slug)


@dashboard_app.route('/<slug>', method='DELETE')
def dashboard_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
