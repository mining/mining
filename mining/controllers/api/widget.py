#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin

from mining.utils import conf
from .base import get, post, put, delete

collection = 'widget'

widget_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
widget_app.install(mongo)


@widget_app.route('/', method='GET')
@widget_app.route('/<slug>', method='GET')
def widget_get(mongodb, slug=None):
    return get(mongodb, collection, slug)


@widget_app.route('/', method='POST')
def widget_post(mongodb, slug=None):
    return post(mongodb, collection)


@widget_app.route('/<slug>', method='PUT')
def widget_put(mongodb, slug=None):
    return put(mongodb, collection, slug)


@widget_app.route('/<slug>', method='DELETE')
def widget_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
