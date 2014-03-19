#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from bottle.ext.mongo import MongoPlugin

from settings import MONGO_URI, RIAK_PROTOCOL, RIAK_HTTP_PORT
from settings import RIAK_HOST, MINING_BUCKET_NAME
from .base import get, post, put, delete

import riak
import json

ADMIN_BUCKET_NAME = 'openminig-admin'
collection = 'element'

element_app = Bottle()
mongo = MongoPlugin(uri=MONGO_URI, db=ADMIN_BUCKET_NAME,
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
def element_get(mongodb, slug=None):
    MyClient = riak.RiakClient(protocol=RIAK_PROTOCOL,
                               http_port=RIAK_HTTP_PORT,
                               host=RIAK_HOST)
    MyBucket = MyClient.bucket(MINING_BUCKET_NAME)
    data = MyBucket.get(u'{}-columns'.format(slug)).data or '{}'
    columns = json.loads(data)
    return {'columns':columns}