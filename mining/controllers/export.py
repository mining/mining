#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import json
import gc
import riak

from bottle import Bottle, request, response
from bottle.ext.mongo import MongoPlugin

from pandas import DataFrame

from mining.settings import PROJECT_PATH
from mining.utils import df_generate, conf, DataFrameSearchColumn


export_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
export_app.install(mongo)


@export_app.route('/data/<slug>.<ext>')
def data(mongodb, slug, ext='xls'):
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

    filters = [i[0] for i in request.GET.iteritems()
               if len(i[0].split('filter__')) > 1]

    df = DataFrame(MyBucket.get(element.get('cube')).data, columns=fields)
    if len(filters) >= 1:
        for f in filters:
            s = f.split('__')
            field = s[1]
            operator = s[2]
            value = request.GET.get(f)
            if operator in ['like', 'regex']:
                df = DataFrameSearchColumn(df, field, value, operator)
            else:
                df = df.query(df_generate(df, value, f))

    groupby = []
    if request.GET.get('groupby', None):
        groupby = request.GET.get('groupby', ).split(',')
    if len(groupby) >= 1:
        df = df.groupby(groupby)

    if request.GET.get('orderby', None):
        orderby = request.GET.get('orderby', [])
        orderby__order = True
        if request.GET.get('orderby__order', 0) != 1:
            orderby__order = False
        df = df.sort(orderby, ascending=orderby__order)

    # CLEAN MEMORY
    del filters, fields, columns
    gc.collect()

    file_name = '{}/assets/exports/openmining-{}.{}'.format(
        PROJECT_PATH, element.get('cube'), ext)
    if ext == 'csv':
        df.to_csv(file_name)
        contenttype = 'text/csv'
    else:
        df.to_excel(file_name)
        contenttype = 'application/vnd.ms-excel'

    response.set_header('charset', 'utf-8')
    response.set_header('Content-disposition', 'attachment; '
                        'filename={}.{}'.format(element.get('cube'), ext))
    response.content_type = contenttype

    ifile = open(file_name, "r")
    o = ifile.read()
    ifile.close()
    return o
