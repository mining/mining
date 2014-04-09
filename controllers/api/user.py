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

from bottle import Bottle, request, redirect
from bottle.ext.mongo import MongoPlugin

from utils import conf
from .base import get, post, put, delete

collection = 'user'

user_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
user_app.install(mongo)


@user_app.route('/session', method='GET')
def session(mongodb):
    session = dict(request.environ.get('beaker.session'))
    return json.dumps(session)


@user_app.route('/login', method='POST')
def login(mongodb):
    login = request.POST
    if request.content_type == "application/json":
        login = request.json
    else:
        login = request.POST

    session = request.environ.get('beaker.session')
    if session.get("username", None) and session.get("apikey", None):
        if request.content_type != "application/json":
            redirect("/login")
        return session

    if login.get("apikey"):
        doc = mongodb[collection].find_one({'username': login['username'],
                                            'apikey': login['apikey']})
    else:
        doc = mongodb[collection].find_one({'username': login['username'],
                                            'password': login['password']})

    if not doc:
        doc = {}
    try:
        doc.pop('_id', None)
    except:
        pass
    try:
        doc.pop('password', None)
    except:
        pass
    session.update(doc)
    session.save()
    if request.content_type != "application/json":
        return redirect('/')
    return doc


@user_app.route('/logout')
def logout(mongodb):

    session = request.environ.get('beaker.session')
    session.delete()
    return redirect('/login')


@user_app.route('/', method='GET')
@user_app.route('/<slug>', method='GET')
def user_get(mongodb, slug=None):
    _get = json.loads(get(mongodb, collection, slug, {'key':'username'}))
    if slug:
        _get.pop('password', None)
        _get.pop('apikey', None)
        return json.dumps(_get)
    else:
        data = []
        for _g in _get:
            _g.pop('password', None)
            _g.pop('apikey', None)
            data.append(_g)
        return json.dumps(data)


@user_app.route('/', method='POST')
def user_post(mongodb, slug=None):
    new_uuid = uuid.uuid4()
    opt = {}
    opt['apikey'] = hmac.new(new_uuid.bytes, digestmod=sha1).hexdigest()
    return post(mongodb, collection, opt,
                {'key': 'username', 'value': 'username'})


@user_app.route('/<slug>', method='PUT')
def user_put(mongodb, slug=None):
    data = request.json
    data.pop("apikey", None)
    return put(mongodb, collection, slug, field={'key': 'username'},
               request_json=data)


@user_app.route('/<slug>', method='DELETE')
def user_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug, {'key': 'username', 'value': 'username'})
