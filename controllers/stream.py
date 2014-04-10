#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import gc
import riak

from bottle import Bottle, abort, request
from bottle.ext.websocket import websocket
from bottle.ext.mongo import MongoPlugin

from pandas import DataFrame

from utils import df_generate, conf


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

    MyClient = riak.RiakClient(protocol=conf("riak")["protocol"],
                               http_port=conf("riak")["http_port"],
                               host=conf("riak")["host"])

    MyBucket = MyClient.bucket(conf("riak")["bucket"])

    element = mongodb['element'].find_one({'slug': slug})

    columns = json.loads(MyBucket.get(
        '{}-columns'.format(element.get('cube'))).data or [])

    fields = columns
    if request.GET.get('fields', None):
        fields = request.GET.get('fields').split(',')
    cube_last_update = mongodb['cube'].find_one({'slug':element.get('cube')})
    ws.send(json.dumps({'type': 'last_update', 'data': str(cube_last_update.get('lastupdate', ''))}))

    ws.send(json.dumps({'type': 'columns', 'data': fields}))

    filters = [i[0] for i in request.GET.iteritems()
               if len(i[0].split('filter__')) > 1]

    if element['type'] == 'grid':
        page = int(request.GET.get('page', 1))
        page_start = 0
        page_end = 50
        if page >= 2:
            page_end = 50 * page
            page_start = page_end - 50
    else:
        page_start = None
        page_end = None

    df = DataFrame(MyBucket.get(element.get('cube')).data, columns=fields)
    if len(filters) >= 1:
        for f in filters:
            df = df.query(df_generate(df, request.GET.get(f), f))

    groupby = []
    if request.GET.get('groupby', None):
        groupby = request.GET.get('groupby', ).split(',')
    if len(groupby) >= 1:
        df = df.groupby(groupby)

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
