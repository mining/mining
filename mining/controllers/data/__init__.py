# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import json
import gc

from bottle import Bottle, request, response
from bottle.ext.mongo import MongoPlugin

from pandas import DataFrame

from mining.settings import PROJECT_PATH
from mining.utils import conf, __from__
from mining.utils._pandas import df_generate, DataFrameSearchColumn
from mining.db import DataWarehouse
from mining.settings import HAS_GEO

if HAS_GEO:
    import shapely.wkt
    from geopandas import GeoDataFrame, GeoSeries


data_app = Bottle()
mongo = MongoPlugin(
    uri=conf("mongodb")["uri"],
    db=conf("mongodb")["db"],
    json_mongo=True)
data_app.install(mongo)


@data_app.route('/<slug>')
def data(mongodb, slug):
    # check protocol to work
    ws = request.environ.get('wsgi.websocket')
    protocol = "websocket"
    if not ws:
        response.content_type = 'application/json'
        protocol = "http"
    DataManager = __from__(
        "mining.controllers.data.{}.DataManager".format(protocol))

    # instantiates the chosen protocol
    DM = DataManager(ws)

    # instantiate data warehouse
    DW = DataWarehouse()

    element = mongodb['element'].find_one({'slug': slug})

    element['page_limit'] = 50
    if request.GET.get('limit', True) is False:
        element['page_limit'] = 9999999999

    if element['type'] == 'grid' and "download" not in request.GET.keys():
        page = int(request.GET.get('page', 1))
        page_start = 0
        page_end = element['page_limit']
        if page >= 2:
            page_end = element['page_limit'] * page
            page_start = page_end - element['page_limit']
    else:
        page = 1
        page_start = None
        page_end = None

    filters = [i[0] for i in request.GET.iteritems()
               if len(i[0].split('filter__')) > 1]

    if not DW.search:
        data = DW.get(element.get('cube'), page=page)
    else:
        data = DW.get(element.get('cube'), filters=filters, page=page)

    columns = data.get('columns') or []

    fields = columns
    if request.GET.get('fields', None):
        fields = request.GET.get('fields').split(',')

    cube_conf = mongodb['cube'].find_one({'slug': element.get('cube')})
    DM.send(json.dumps({'type': 'last_update',
                        'data': str(cube_conf.get('lastupdate', ''))}))

    DM.send(json.dumps({'type': 'columns', 'data': fields}))

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
        groupby = request.GET.get('groupby', "").split(',')
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

    DM.send(json.dumps({'type': 'max_page',
                        'data': data.get('count', len(df))}))

    # CLEAN MEMORY
    del filters, columns
    gc.collect()
    categories = []

    records = df.to_dict(orient='records')
    if not DW.search:
        records = records[page_start:page_end]
    for i in records:
        if element.get('categories', None):
            categories.append(i[element.get('categories')])
        DM.send(json.dumps({'type': 'data', 'data': i}))

    DM.send(json.dumps({'type': 'categories', 'data': categories}))
    DM.send(json.dumps({'type': 'close'}))

    # CLEAN MEMORY
    del categories
    gc.collect()

    if not ws:
        if "download" in request.GET.keys():

            ext = request.GET.get("download", "xls")
            if ext == '':
                ext = 'xls'

            file_name = '{}/frontend/assets/exports/openmining-{}.{}'.format(
                PROJECT_PATH, element.get('cube'), ext)
            if ext == 'csv':
                df.to_csv(file_name, sep=";")
                contenttype = 'text/csv'
            elif ext == 'geojson' and \
                    HAS_GEO and 'spatial' in cube_conf.get('type'):

                geom_col = 'geom'

                wkt_geoms = df[geom_col]
                s = wkt_geoms.apply(lambda x: shapely.wkt.loads(x))
                df[geom_col] = GeoSeries(s)
                df = GeoDataFrame(df, geometry=geom_col, columns=fields)

                o = df.to_json()
                # TODO: Refactor in order to serve directly from memory
                # without saving on disk
                ifile = open(file_name, "w")
                ifile.write(o)
                ifile.close()
                contenttype = ' application/vnd.geo+json'
            else:
                df.to_excel(file_name)
                contenttype = 'application/vnd.ms-excel'

            response.set_header('charset', 'utf-8')
            response.set_header('Content-disposition', 'attachment; '
                                'filename={}.{}'.format(
                                    element.get('cube'), ext))
            response.content_type = contenttype

            ifile = open(file_name, "r")
            o = ifile.read()
            ifile.close()

            return o

        return json.dumps(DM.data)
