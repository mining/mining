# !/usr/bin/env python
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

from mining.utils import conf, parse_dumps
from mining.controllers.api.group import collection as permission_group
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
    else:
        doc['uid'] = doc['username']

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
    return redirect('/')


@user_app.route('/', method='GET')
@user_app.route('/<slug>', method='GET')
def user_get(mongodb, slug=None):
    obj = json.loads(get(mongodb, collection, slug, {'key': 'username'}))
    if type(obj) is dict and len(obj.keys()) >= 1:
        _get = obj
        _get['uid'] = _get['username']
    elif slug and len(obj.keys()) == 0:
        _get = {
            'uid': slug,
            'username': slug,
            'new_user': True
        }
    else:
        _get = []
        for i in obj:
            i['uid'] = i['username']
            _get.append(i)

    if slug:
        _get.pop('password', None)
        _get.pop('apikey', None)
        _get['is_admin_group'] = False
        groups = mongodb[permission_group].find({
            'admins.id': {
                '$in': [_get.get('username', '')]
            }
        })
        if groups:
            _get['is_admin_group'] = list(groups)
        return json.dumps(_get, default=parse_dumps)
    else:
        data = []
        for _g in _get:
            _g.pop('password', None)
            _g.pop('apikey', None)
            data.append(_g)
        return json.dumps(data, default=parse_dumps)


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
    return delete(mongodb, collection, slug, {'key': 'username',
                                              'value': 'username'})
