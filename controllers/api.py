#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, response, request

from riak import RiakClient


api_app = Bottle()
ADMIN_BUCKET_NAME = 'openminig-admin'


def api_base():
    response.set_header('charset', 'utf-8')
    response.content_type = 'application/json'


def api_get(str_bucket, slug=None):
    rclient = RiakClient(protocol='http', http_port=8098,
                         host='127.0.0.1')
    MyAdminBucket = rclient.bucket(ADMIN_BUCKET_NAME)

    bucket = MyAdminBucket.get(str_bucket).data or []

    if slug:
        value = {}
        for i in bucket:
            if i.get('slug') == slug:
                value = i
        bucket = value

    return bucket


@api_app.route('/')
def index():
    return 'OpenMining API!'


@api_app.route('/connection/:slug')
@api_app.route('/connection/')
def connection_get(slug=None):
    return api_get('connection', slug)
