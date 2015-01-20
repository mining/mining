#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin

from mining.utils import conf
from mining.db import DataWarehouse
from .base import get, post, put, delete


collection = 'element'

element_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
element_app.install(mongo)


@element_app.route('/', method='GET')
@element_app.route('/<slug>', method='GET')
def element_get(mongodb, slug=None):
    return get(mongodb, collection, slug)


@element_app.route('/', method='POST')
def element_post(mongodb, slug=None):
    return post(mongodb, collection)


@element_app.route('/<slug>', method='PUT')
def element_put(mongodb, slug=None):
    return put(mongodb, collection, slug)


@element_app.route('/<slug>', method='DELETE')
def element_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)


@element_app.route('/cube/<slug>', method='GET')
def element_cube(mongodb, slug=None):
    DW = DataWarehouse()
    data = DW.get(slug)
    columns = data.get("columns") or []
    return {'columns': columns}
