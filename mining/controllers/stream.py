#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey

monkey.patch_all()

import json
import gc

from bottle import Bottle, abort, request
from bottle.ext.websocket import websocket
from bottle.ext.mongo import MongoPlugin

from pandas import DataFrame

from mining.utils import conf
from mining.utils._pandas import df_generate, DataFrameSearchColumn
from mining.db.datawarehouse import DataWarehouse


stream_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
stream_app.install(mongo)


@stream_app.route('/data/<slug>', apply=[websocket])
def data(ws, mongodb, slug):
    if not ws:
        abort(400, 'Expected WebSocket request.')

    DW = DataWarehouse()

    element = mongodb['element'].find_one({'slug': slug})

    element['page_limit'] = 50
    if request.GET.get('limit', True) is False:
        element['page_limit'] = 9999999999

    data = DW.get(element.get('cube'))
    columns = data.get('columns') or []

    fields = columns
    if request.GET.get('fields', None):
        fields = request.GET.get('fields').split(',')

    cube_last_update = mongodb['cube'].find_one({'slug': element.get('cube')})
    ws.send(json.dumps({'type': 'last_update',
                        'data': str(cube_last_update.get('lastupdate', ''))}))

    ws.send(json.dumps({'type': 'columns', 'data': fields}))

    filters = [i[0] for i in request.GET.iteritems()
               if len(i[0].split('filter__')) > 1]

    if element['type'] == 'grid':
        page = int(request.GET.get('page', 1))
        page_start = 0
        page_end = element['page_limit']
        if page >= 2:
            page_end = element['page_limit'] * page
            page_start = page_end - element['page_limit']
    else:
        page_start = None
        page_end = None

    df = DataFrame(data.get('data') or {}, columns=fields)
    if len(filters) >= 1:
        for f in filters:
            s = f.split('__')
            field = s[1]
            operator = s[2]
            value = request.GET.get(f)
            if operator == 'like':
                df = df[df[field].str.contains(value)]
            elif operator == 'regex':
                df = DataFrameSearchColumn(df, field, value, operator)
            else:
                df = df.query(df_generate(df, value, f))

    groupby = []
    if request.GET.get('groupby', None):
        groupby = request.GET.get('groupby', ).split(',')
    if len(groupby) >= 1:
        df = DataFrame(df.groupby(groupby).grouper.get_group_levels())

    if request.GET.get('orderby',
                       element.get('orderby', None)) and request.GET.get(
            'orderby', element.get('orderby', None)) in fields:

        orderby = request.GET.get('orderby', element.get('orderby', ''))
        if type(orderby) == str:
            orderby = orderby.split(',')
        orderby__order = request.GET.get('orderby__order',
                                         element.get('orderby__order', ''))
        if type(orderby__order) == str:
            orderby__order = orderby__order.split(',')
        ind = 0
        for orde in orderby__order:
            if orde == '0':
                orderby__order[ind] = False
            else:
                orderby__order[ind] = True
            ind += 1
        df = df.sort(orderby, ascending=orderby__order)

    ws.send(json.dumps({'type': 'max_page', 'data': len(df)}))

    # CLEAN MEMORY
    del filters, fields, columns
    gc.collect()
    categories = []
    for i in df.to_dict(outtype='records')[page_start:page_end]:
        if element.get('categories', None):
            categories.append(i[element.get('categories')])
        ws.send(json.dumps({'type': 'data', 'data': i}))

    # CLEAN MEMORY
    del df
    gc.collect()

    ws.send(json.dumps({'type': 'categories', 'data': categories}))
    ws.send(json.dumps({'type': 'close'}))

    # CLEAN MEMORY
    del categories
    gc.collect()
