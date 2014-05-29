#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin

from mining.utils import conf
from .base import get, post, put, delete

collection = 'permissions_group'

permissions_group_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
permissions_group_app.install(mongo)


@permissions_group_app.route('/', method='GET')
@permissions_group_app.route('/<slug>', method='GET')
def group_get(mongodb, slug=None):
    return get(mongodb, collection, slug)


@permissions_group_app.route('/', method='POST')
def group_post(mongodb, slug=None):
    return post(mongodb, collection)


@permissions_group_app.route('/<slug>', method='PUT')
def group_put(mongodb, slug=None):
    return put(mongodb, collection, slug)


@permissions_group_app.route('/<slug>', method='DELETE')
def group_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
