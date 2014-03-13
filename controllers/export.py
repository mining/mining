#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import gc
import riak

from bottle import Bottle, request, response
from bottle.ext.mongo import MongoPlugin

from pandas import DataFrame

from utils import df_generate
from settings import RIAK_PROTOCOL, RIAK_HTTP_PORT, RIAK_HOST
from settings import MINING_BUCKET_NAME, ADMIN_BUCKET_NAME, PROJECT_PATH


MyClient = riak.RiakClient(protocol=RIAK_PROTOCOL,
                           http_port=RIAK_HTTP_PORT,
                           host=RIAK_HOST)

MyBucket = MyClient.bucket(MINING_BUCKET_NAME)


export_app = Bottle()
mongo = MongoPlugin(uri="mongodb://127.0.0.1", db=ADMIN_BUCKET_NAME,
                    json_mongo=True)

export_app.install(mongo)


@export_app.route('/')
def data(mongodb, slug, ext='xls'):
    columns = json.loads(MyBucket.get('{}-columns'.format(slug)).data)
    fields = columns
    if request.GET.get('fields', None):
        fields = request.GET.get('fields').split(',')

    filters = [i[0] for i in request.GET.iteritems()
               if len(i[0].split('filter__')) > 1]

    df = DataFrame(MyBucket.get(slug).data, columns=fields)
    if len(filters) >= 1:
        for f in filters:
            df = df.query(df_generate(df, request.GET.get(f), f))

    # CLEAN MEMORY
    del filters, fields, columns
    gc.collect()

    file_name = '{}/assets/exports/openmining-{}.{}'.format(
        PROJECT_PATH, slug, ext)
    if ext == 'csv':
        df.to_csv(file_name)
        contenttype = 'text/csv'
    else:
        df.to_excel(file_name)
        contenttype = 'application/vnd.ms-excel'

    response.set_header('charset', 'utf-8')
    response.set_header('Content-disposition', 'attachment; '
                        'filename={}.{}'.format(slug, ext))
    response.content_type = contenttype

    ifile = open(file_name, "r")
    o = ifile.read()
    ifile.close()
    return o
