#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import sys, path
import json
import riak
import gc
from datetime import datetime
from threading import Thread

from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from utils import fix_render, conf, log_it

from bottle.ext.mongo import MongoPlugin


def run(cube_slug=None):
    mongo = MongoPlugin(
        uri=conf("mongodb")["uri"],
        db=conf("mongodb")["db"],
        json_mongo=True).get_mongo()

    for cube in mongo['cube'].find():
        slug = cube['slug']
        if cube_slug and cube_slug != slug:
            continue

        if cube.get('run') == 'run':
            log_it("PROCESS {} IN RUN, NOT YET FINISHED".format(slug),
                   "bin-mining")
            continue

        Thread(target=process, args=(cube, mongo)).start()

    return True


def process(_cube, mongo):
    log_it("START: {}".format(_cube['slug']), "bin-mining")
    MyClient = riak.RiakClient(
        protocol=conf("riak")["protocol"],
        http_port=conf("riak")["http_port"],
        host=conf("riak")["host"])

    MyBucket = MyClient.bucket(conf("riak")["bucket"])
    cube = _cube

    try:
        cube['run'] = 'run'
        mongo['cube'].update({'slug': cube['slug']}, cube)

        cube['start_process'] = datetime.now()
        slug = cube['slug']

        _sql = cube['sql']
        if _sql[-1] == ';':
            _sql = _sql[:-1]
        sql = u"""SELECT * FROM ({}) AS CUBE;""".format(_sql)

        connection = mongo['connection'].find_one({
            'slug': cube['connection']})['connection']

        log_it("CONNECT IN RELATION DATA BASE: {}".format(slug),
               "bin-mining")
        e = create_engine(connection, pool_timeout=580, pool_size=100,
                          max_overflow=100)
        Session = sessionmaker(bind=e)
        session = Session()

        resoverall = session.execute(text(sql))

        log_it("LOAD DATA ON DATAWAREHOUSE: {}".format(slug),
               "bin-mining")
        df = DataFrame(resoverall.fetchall())
        if df.empty:
            log_it('[warnning]Empty cube: {}!!'.format(cube),
                   "bin-mining")
            return
        df.columns = resoverall.keys()
        df.head()

        pdict = map(fix_render, df.to_dict(outtype='records'))

        MyBucket.new(slug, data='').store()
        MyBucket.new(u'{}-columns'.format(slug), data='').store()
        MyBucket.new(u'{}-connect'.format(slug), data='').store()
        MyBucket.new(u'{}-sql'.format(slug), data='').store()

        log_it("SAVE DATA (JSON) ON RIAK: {}".format(slug),
               "bin-mining")
        MyBucket.new(slug, data=pdict).store()

        log_it("SAVE COLUMNS ON RIAK: {}".format(slug),
               "bin-mining")
        MyBucket.new(u'{}-columns'.format(slug),
                     data=json.dumps([c for c in df.columns])).store()

        log_it("SAVE CONNECT ON RIAK: {}".format(slug),
               "bin-mining")
        MyBucket.new(u'{}-connect'.format(slug), data=c).store()

        log_it("SAVE SQL ON RIAK: {}".format(slug),
               "bin-mining")
        MyBucket.new(u'{}-sql'.format(slug), data=sql).store()

        cube['status'] = True
        cube['lastupdate'] = datetime.now()
        cube['run'] = True
        mongo['cube'].update({'slug': cube['slug']}, cube)

        log_it("CLEAN MEMORY: {}\n".format(slug), "bin-mining")
        del pdict, df
        gc.collect()
    except Exception, e:
        log_it(e, "bin-mining")
        _cube['run'] = False
        mongo['cube'].update({'slug': _cube['slug']}, _cube)

    log_it("END: {}".format(_cube['slug']), "bin-mining")


if __name__ == "__main__":
    run()
