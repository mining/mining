#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from bottle import Bottle, request
from bottle.ext.mongo import MongoPlugin

from utils import conf
from .base import get, post, put, delete

from element import collection as collection_element
from cube import collection as collection_cube
from filter import collection as collection_filter

collection = 'dashboard'

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
    def full_elements(das):
        if 'element' in das:
            elements = das['element']
            das['element'] = []
            for el in elements:
                n_el = mongodb[collection_element].find_one({'slug': el})
                if n_el:
                    del n_el['_id']
                    _cube = mongodb[collection_cube].find_one({'slug':n_el['cube']},
                                                              {
                                                                  'name':True,
                                                                  'slug':True,
                                                                  'lastupdate':True,
                                                                  'scheduler_status':True,
                                                                  'scheduler_interval':True,
                                                                  'scheduler_type':True
                                                              })
                    if _cube:
                        del _cube['_id']
                        _cube['lastupdate'] = str(_cube.get('lastupdate','')).replace(' ', 'T')
                        n_el['cube']=_cube
                    _filters = mongodb[collection_filter].find({'element':n_el['slug']})
                    if _filters:
                        _fil = []
                        for x in _filters:
                            x.pop('_id', None)
                            _fil.append(x)
                        print _fil
                        n_el['saved_filters'] = _fil
                    das['element'].append(n_el)
        return das
    if slug:
        return json.dumps(full_elements(response))
    for r in response:
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
