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
from settings import MINING_BUCKET_NAME, ADMIN_BUCKET_NAME


MyClient = riak.RiakClient(protocol=RIAK_PROTOCOL,
                           http_port=RIAK_HTTP_PORT,
                           host=RIAK_HOST)

MyBucket = MyClient.bucket(MINING_BUCKET_NAME)


stream_app = Bottle()
mongo = MongoPlugin(uri="mongodb://127.0.0.1", db=ADMIN_BUCKET_NAME,
                    json_mongo=True)

stream_app.install(mongo)


@stream_app.route('/data/<slug>', apply=[websocket])
def data(ws, mongodb, slug):
    if not ws:
        abort(400, 'Expected WebSocket request.')

    columns = json.loads(MyBucket.get('{}-columns'.format(slug)).data)
    fields = columns
    if request.GET.get('fields', None):
        fields = request.GET.get('fields').split(',')

    ws.send({'type': 'columns', 'data': fields})

    filters = [i[0] for i in request.GET.iteritems()
               if len(i[0].split('filter__')) > 1]

    try:
        ca = mongo['element'].find_one({'slug': slug})['categories']
    except:
        ca = None

    page = int(request.GET.get('page', 1))
    page_start = 0
    page_end = 50
    if page >= 2:
        page_end = 50 * page
        page_start = page_end - 50

    df = DataFrame(MyBucket.get(slug).data, columns=fields)
    if len(filters) >= 1:
        for f in filters:
            df = df.query(df_generate(df, request.GET.get(f), f))
    ws.send({'type': 'max_page', 'data': len(df)})

    # CLEAN MEMORY
    del filters, fields, columns
    gc.collect() 
    categories = []
    for i in df.to_dict(outtype='records')[page_start:page_end]:
        if ca:
            categories.append(i[ca])
        ws.send({'type': 'data', 'data': i})

    # CLEAN MEMORY
    del df
    gc.collect()

    ws.send({'type': 'categories', 'data': categories})
    ws.send({'type': 'close'})

    # CLEAN MEMORY
    del categories
    gc.collect()
