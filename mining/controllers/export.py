#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import json
import gc

from bottle import Bottle, request, response
from bottle.ext.mongo import MongoPlugin

from pandas import DataFrame

from mining.settings import PROJECT_PATH
from mining.utils import conf
from mining.utils._pandas import df_generate, DataFrameSearchColumn
from mining.db.datawarehouse import DataWarehouse


export_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
export_app.install(mongo)


@export_app.route('/data/<slug>.<ext>')
def data(mongodb, slug, ext='xls'):
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

    filters = [i[0] for i in request.GET.iteritems()
               if len(i[0].split('filter__')) > 1]

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

    # CLEAN MEMORY
    del filters, fields, columns
    gc.collect()

    file_name = '{}/assets/exports/openmining-{}.{}'.format(
        PROJECT_PATH, element.get('cube'), ext)
    if ext == 'csv':
        df.to_csv(file_name, sep=";")
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
