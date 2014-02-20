#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import sys, path
import json
import riak
import memcache

from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.sql import text

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from utils import fix_render
from settings import (RIAK_PROTOCOL, RIAK_HTTP_PORT,
                      RIAK_HOST, ADMIN_BUCKET_NAME,
                      MINING_BUCKET_NAME, MEMCACHE_CONNECTION, MEMCACHE_DEBUG)


MyClient = riak.RiakClient(protocol=RIAK_PROTOCOL,
                           http_port=RIAK_HTTP_PORT,
                           host=RIAK_HOST)

MyAdminBucket = MyClient.bucket(ADMIN_BUCKET_NAME)

MyBucket = MyClient.bucket(MINING_BUCKET_NAME)


def run(cube_slug=None):
    for cube in MyAdminBucket.get('cube').data:
        try:
            slug = cube['slug']

            if cube_slug and cube_slug != slug:
                continue

            sql = """SELECT * FROM ({}) AS CUBE;""".format(cube['sql'])
            for c in MyAdminBucket.get('connection').data:
                if c['slug'] == cube['conection']:
                    connection = c['conection']

            print "\n# CLEAN MEMCACHE/RIAK: {}".format(slug)
            mc = memcache.Client(['127.0.0.1:11211'], debug=0)
            mc.delete(str(slug))
            mc.delete(str('{}-columns'.format(slug)))

            MyBucket.new(slug, data='').store()
            MyBucket.new(u'{}-columns'.format(slug), data='').store()
            MyBucket.new(u'{}-connect'.format(slug), data='').store()
            MyBucket.new(u'{}-sql'.format(slug), data='').store()

            print "# CONNECT IN RELATION DATA BASE: {}".format(slug)
            e = create_engine(connection)
            connection = e.connect()

            resoverall = connection.execute(text(sql))

            print "# LOAD DATA ON DATAWAREHOUSE: {}".format(slug)
            df = DataFrame(resoverall.fetchall())
            if df.empty:
                print '[warnning]Empty cube: {}!!'.format(cube)
                return
            df.columns = resoverall.keys()
            df.head()

            pdict = map(fix_render, df.to_dict(outtype='records'))

            print "# SAVE DATA (JSON) ON RIAK: {}".format(slug)
            MyBucket.new(slug, data=pdict).store()

            print "# SAVE COLUMNS ON RIAK: {}".format(slug)
            MyBucket.new(u'{}-columns'.format(slug),
                         data=json.dumps([c for c in df.columns])).store()

            print "# SAVE CONNECT ON RIAK: {}".format(slug)
            MyBucket.new(u'{}-connect'.format(slug), data=c).store()

            print "# SAVE SQL ON RIAK: {}\n".format(slug)
            MyBucket.new(u'{}-sql'.format(slug), data=sql).store()
        except:
            pass

    print "## FINISH"
    return True


if __name__ == "__main__":
    run()
