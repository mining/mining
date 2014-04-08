#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin

from utils import conf
from .base import get, post, put, delete


collection = 'filter'

filter_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
filter_app.install(mongo)


@filter_app.route('/', method='GET')
@filter_app.route('/<slug>', method='GET')
def filter_get(mongodb, slug=None):
    return get(mongodb, collection, slug)


@filter_app.route('/', method='POST')
def filter_post(mongodb, slug=None):
    return post(mongodb, collection)


@filter_app.route('/<slug>', method='PUT')
def filter_put(mongodb, slug=None):
    return put(mongodb, collection, slug)


@filter_app.route('/<slug>', method='DELETE')
def filter_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
