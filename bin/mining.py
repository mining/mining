#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import sys, path
import json
import riak
import gc
from datetime import datetime

from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.sql import text

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from utils import fix_render, conf

from bottle.ext.mongo import MongoPlugin


def run(cube_slug=None):
    mongo = MongoPlugin(
        uri=conf("mongodb")["uri"],
        db=conf("mongodb")["db"],
        json_mongo=True).get_mongo()

    MyClient = riak.RiakClient(
        protocol=conf("riak")["protocol"],
        http_port=conf("riak")["http_port"],
        host=conf("riak")["host"])

    MyBucket = MyClient.bucket(conf("riak")["bucket"])

    print "## START"
    for cube in mongo['cube'].find():
        try:
            slug = cube['slug']

            if cube_slug and cube_slug != slug:
                continue

            sql = u"""SELECT * FROM ({}) AS CUBE;""".format(cube['sql'])

            connection = mongo['connection'].find_one({
                'slug': cube['connection']})['connection']

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

            print "# SAVE SQL ON RIAK: {}".format(slug)
            MyBucket.new(u'{}-sql'.format(slug), data=sql).store()

            cube['status'] = True
            cube['lastupdate'] = datetime.now()
            mongo['cube'].update({'slug': cube['slug']}, cube)

            print "# CLEAN MEMORY: {}\n".format(slug)
            del pdict, df
            gc.collect()
        except Exception, e:
            print e
            # pass

    print "## END"
    return True


if __name__ == "__main__":
    run()
