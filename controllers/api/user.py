#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import hmac
import json

try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.sha

from bottle import Bottle, request
from bottle.ext.mongo import MongoPlugin
from beaker.middleware import SessionMiddleware

from utils import conf
from .base import get, post, put, delete

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

collection = 'user'

user_app = SessionMiddleware(Bottle(), session_opts)
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
user_app.wrap_app.install(mongo)


@user_app.wrap_app.route('/login', method='POST')
def login(mongodb):

    login = request.POST
    if request.content_type == "application/json":
        login = request.json

    session = request.environ.get('beaker.session')
    if session.get("username", None) and session.get("apikey", None):
        return session

    if login.get("apikey"):
        doc = mongodb[collection].find_one({'username': login['username'],
                                            'apikey': login['apikey']})
    else:
        doc = mongodb[collection].find_one({'username': login['username'],
                                            'password': login['password']})
    doc.pop('_id', None)
    doc.pop('password', None)
    session.update(doc)
    session.save()
    return doc


@user_app.wrap_app.route('/', method='GET')
@user_app.wrap_app.route('/<slug>', method='GET')
def user_get(mongodb, slug=None):
    _get = json.loads(get(mongodb, collection, slug))
    data = []
    for _g in _get:
        _g.pop('password', None)
        _g.pop('apikey', None)
        data.append(_g)
    return json.dumps(data)


@user_app.wrap_app.route('/', method='POST')
def user_post(mongodb, slug=None):
    new_uuid = uuid.uuid4()
    opt = {}
    opt['apikey'] = hmac.new(new_uuid.bytes, digestmod=sha1).hexdigest()
    return post(mongodb, collection, opt,
                {'key': 'username', 'value': 'username'})


@user_app.wrap_app.route('/<slug>', method='PUT')
def user_put(mongodb, slug=None):
    data = request.json
    data.pop("apikey", None)
    return put(mongodb, collection, slug, field={'key': 'username'},
               request_json=data)


@user_app.wrap_app.route('/<slug>', method='DELETE')
def user_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)
