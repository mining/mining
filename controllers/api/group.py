#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin

from utils import conf
from .base import get, post, put, delete

collection = 'group'

group_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
group_app.install(mongo)


@group_app.route('/', method='GET')
@group_app.route('/<slug>', method='GET')
def group_get(mongodb, slug=None):
    return get(mongodb, collection, slug)


@group_app.route('/', method='POST')
def group_post(mongodb, slug=None):
    return post(mongodb, collection)


@group_app.route('/<slug>', method='PUT')
def group_put(mongodb, slug=None):
    return put(mongodb, collection, slug)


@group_app.route('/<slug>', method='DELETE')
def group_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
