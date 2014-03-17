#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import gc
import riak

from bottle import Bottle, abort, request
from bottle.ext.websocket import websocket
from bottle.ext.mongo import MongoPlugin

from pandas import DataFrame

from utils import df_generate
from settings import RIAK_PROTOCOL, RIAK_HTTP_PORT, RIAK_HOST
from settings import MINING_BUCKET_NAME, ADMIN_BUCKET_NAME, MONGO_URI


stream_app = Bottle()
mongo = MongoPlugin(uri=MONGO_URI, db=ADMIN_BUCKET_NAME, json_mongo=True)
stream_app.install(mongo)


@stream_app.route('/data/<slug>', apply=[websocket])
def data(ws, mongodb, slug):

    if not ws:
        abort(400, 'Expected WebSocket request.')

    MyClient = riak.RiakClient(protocol=RIAK_PROTOCOL,
                               http_port=RIAK_HTTP_PORT,
                               host=RIAK_HOST)

    MyBucket = MyClient.bucket(MINING_BUCKET_NAME)

    element = mongodb['element'].find_one({'slug': slug})

    columns = json.loads(MyBucket.get(
        '{}-columns'.format(element.get('cube'))).data or [])

    fields = columns
    if request.GET.get('fields', None):
        fields = request.GET.get('fields').split(',')

    ws.send(json.dumps({'type': 'columns', 'data': fields}))

    filters = [i[0] for i in request.GET.iteritems()
               if len(i[0].split('filter__')) > 1]

    page = int(request.GET.get('page', 1))
    page_start = 0
    page_end = 50
    if page >= 2:
        page_end = 50 * page
        page_start = page_end - 50

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
