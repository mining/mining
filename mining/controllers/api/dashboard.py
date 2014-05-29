# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from bottle import Bottle, request
from bottle.ext.mongo import MongoPlugin

from mining.utils import conf, parse_dumps
from .base import get, post, put, delete, base

from element import collection as collection_element
from cube import collection as collection_cube
from filter import collection as collection_filter
from group import collection as collection_permissions_group

collection = 'dashboard'
collection_group = '{}_groups'.format(collection)

dashboard_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
dashboard_app.install(mongo)


@dashboard_app.route('/', method='GET')
@dashboard_app.route('/<slug>', method='GET')
def dashboard_get(mongodb, slug=None):
    da = get(mongodb, collection, slug)
    if 'full' not in request.GET:
        return da
    response = json.loads(da)
    new_resp = []
    session = dict(request.environ.get('beaker.session'))

    def full_elements(das, permited_elements=None):
        if 'element' in das:
            elements = das['element']
            das['element'] = []
            if session.get('rule', '') == 'admin' and permited_elements:
                elements = permited_elements
            for el in elements:
                new_el = mongodb[collection_element].find_one({
                    'slug': el['id'] if type(el) == dict else el
                })
                if new_el:
                    del new_el['_id']
                    _cube = mongodb[collection_cube].find_one(
                        {'slug': new_el['cube']},
                        {
                            'name': True,
                            'slug': True,
                            'lastupdate': True,
                            'scheduler_status': True,
                            'scheduler_interval': True,
                            'scheduler_type': True
                        })
                    if _cube:
                        del _cube['_id']
                        _cube['lastupdate'] = str(
                            _cube.get('lastupdate', '')).replace(' ', 'T')
                        new_el['cube'] = _cube
                    _filters = mongodb[collection_filter].find(
                        {'element': new_el['slug']})
                    if _filters:
                        _fil = []
                        for x in _filters:
                            x.pop('_id', None)
                            _fil.append(x)
                        new_el['saved_filters'] = _fil
                    das['element'].append(new_el)
        return das

    if slug:
        return json.dumps(full_elements(response))
    for r in response:
        if session.get('rule', '') == 'admin':
            admin_groups = mongodb[collection_permissions_group].find({
                'admins.label': session.get('username', '')}
            )
            for ag in admin_groups:
                if r.get('slug', '') in ag.get('permissions', {}).keys():
                    new_resp.append(
                        full_elements(
                            r,
                            ag.get('permissions', {}).get(r.get('slug', ''),
                                [])
                        )
                    )
        else:
            new_resp.append(full_elements(r))
    return json.dumps(new_resp)


@dashboard_app.route('/', method='POST')
def dashboard_post(mongodb, slug=None):
    return post(mongodb, collection)


@dashboard_app.route('/<slug>', method='PUT')
def dashboard_put(mongodb, slug=None):
    return put(mongodb, collection, slug)


@dashboard_app.route('/<slug>', method='DELETE')
def dashboard_delete(mongodb, slug=None):
    return delete(mongodb, collection, slug)


@dashboard_app.route('/dashboard-group', method='GET')
@dashboard_app.route('/dashboard-group/<slug>', method='GET')
def dashboard_group_get(mongodb, slug=None):
    base()
    _groups = mongodb[collection_group].find()
    groups = []
    for g in _groups:
        del g['_id']
        groups.append(g)
    return json.dumps(groups, default=parse_dumps)


@dashboard_app.route('/dashboard-group', method='POST')
def dashboard_group_post(mongodb, slug=None):
    return post(mongodb, collection_group)


@dashboard_app.route('/dashboard-group/<slug>', method='PUT')
def dashboard_group_put(mongodb, slug=None):
    return put(mongodb, collection_group, slug)


@dashboard_app.route('/dashboard-group/<slug>', method='DELETE')
def dashboard_group_delete(mongodb, slug=None):
    return delete(mongodb, collection_group, slug)
