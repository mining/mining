#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import riak
import memcache

from pandas import DataFrame
from sqlalchemy import create_engine

from utils import pandas_to_dict


myClient = riak.RiakClient(protocol='http',
                           http_port=8098,
                           host='127.0.0.1')
radmin = myClient.bucket('openmining-admin')

for cube in radmin.get('cube').data:
    slug = cube['slug']
    sql = cube['sql']
    for c in radmin.get('connection').data:
        if c['slug'] == cube['conection']:
            connection = c['conection']

    print "# CLEAN MEMCACHE: {}".format(slug)
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    mc.delete(str(slug))
    mc.delete(str('{}-columns'.format(slug)))

    rmining = myClient.bucket('openmining')

    print "# CONNECT IN RELATION DATA BASE: {}".format(slug)
    e = create_engine(connection)
    connection = e.connect()

    resoverall = connection.execute(sql)

    print "# LOAD DATA ON DATAWAREHOUSE: {}".format(slug)
    df = DataFrame(resoverall.fetchall())
    df.columns = resoverall.keys()
    df.head()

    convert = pandas_to_dict(df)

    print "# SAVE DATA (JSON) ON RIAK: {}".format(slug)
    join = json.dumps(convert)
    b1 = rmining.new(slug, data=join)
    b1.store()

    print "# SAVE COLUMNS ON RIAK: {}".format(slug)
    b2 = rmining.new(u'{}-columns'.format(slug),
                     data=json.dumps([c for c in df.columns]))
    b2.store()

    print "# SAVE CONNECT ON RIAK: {}".format(slug)
    b3 = rmining.new(u'{}-connect'.format(slug), data=c)
    b3.store()

    print "# SAVE SQL ON RIAK: {}".format(slug)
    b4 = rmining.new(u'{}-sql'.format(slug), data=sql)
    b4.store()

print "## FINISH"
