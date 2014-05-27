#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import riak
import gc
import traceback
from datetime import datetime

from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

from mining.utils import fix_render, conf, log_it
from mining.multithread import ThreadPool

from bottle.ext.mongo import MongoPlugin


def run(cube_slug=None):
    mongo = MongoPlugin(
        uri=conf("mongodb")["uri"],
        db=conf("mongodb")["db"],
        json_mongo=True).get_mongo()

    pool = ThreadPool(20)

    for cube in mongo['cube'].find():
        slug = cube['slug']
        if cube_slug and cube_slug != slug:
            continue

        pool.add_task(process, cube)

    pool.wait_completion()
    return True


class CubeProcess(object):
    def __init__(self, _cube):

        log_it("START: {}".format(_cube['slug']), "bin-mining")

        self.mongo = MongoPlugin(
            uri=conf("mongodb")["uri"],
            db=conf("mongodb")["db"],
            json_mongo=True).get_mongo()

        MyClient = riak.RiakClient(
            protocol=conf("riak")["protocol"],
            http_port=conf("riak")["http_port"],
            host=conf("riak")["host"])

        self.MyBucket = MyClient.bucket(conf("riak")["bucket"])
        self.MyBucket.enable_search()
        self.cube = _cube
        self.slug = self.cube['slug']

    def load(self):
        self.cube['run'] = 'run'
        self.mongo['cube'].update({'slug': self.slug}, self.cube)

        self.cube['start_process'] = datetime.now()

        _sql = self.cube['sql']
        if _sql[-1] == ';':
            _sql = _sql[:-1]
        self.sql = u"""SELECT * FROM ({}) AS CUBE;""".format(_sql)

        connection = self.mongo['connection'].find_one({
            'slug': self.cube['connection']})['connection']

        log_it("CONNECT IN RELATION DATA BASE: {}".format(self.slug),
               "bin-mining")
        e = create_engine(connection, **conf('openmining')['sql_conn_params'])
        Session = sessionmaker(bind=e)
        session = Session()

        resoverall = session.execute(text(self.sql))
        self.data = resoverall.fetchall()
        self.keys = resoverall.keys()

    def environment(self, t):
        if t not in ['relational']:
            self.sql = t

    def _data(self, data):
        self.data = data

    def _keys(self, keys):
        self.keys = keys

    def frame(self):
        log_it("LOAD DATA ON DATAWAREHOUSE: {}".format(self.slug),
               "bin-mining")
        self.df = DataFrame(self.data)
        if self.df.empty:
            log_it('[warning]Empty cube: {}!!'.format(self.cube),
                   "bin-mining")
            return
        self.df.columns = self.keys
        self.df.head()

        self.pdict = map(fix_render, self.df.to_dict(outtype='records'))

    def clean(self):
        log_it("CLEAN DATA (JSON) ON RIAK: {}".format(self.slug),
               "bin-mining")

        self.MyBucket.new(self.slug, data='').store()
        self.MyBucket.new(u'{}-columns'.format(self.slug), data='').store()
        self.MyBucket.new(u'{}-connect'.format(self.slug), data='').store()
        self.MyBucket.new(u'{}-sql'.format(self.slug), data='').store()

    def save(self):
        self.clean()

        log_it("SAVE DATA (JSON) ON RIAK: {}".format(self.slug),
               "bin-mining")
        self.MyBucket.new(self.slug, data=self.pdict,
                          content_type="application/json").store()

        log_it("SAVE COLUMNS ON RIAK: {}".format(self.slug),
               "bin-mining")
        self.MyBucket.new(u'{}-columns'.format(self.slug), data=json.dumps(
            [c for c in self.df.columns])).store()

        log_it("SAVE CONNECT ON RIAK: {}".format(self.slug),
               "bin-mining")
        self.MyBucket.new(u'{}-connect'.format(self.slug), data=c).store()

        log_it("SAVE SQL ON RIAK: {}".format(self.slug),
               "bin-mining")
        self.MyBucket.new(u'{}-sql'.format(self.slug), data=self.sql).store()

        self.cube['status'] = True
        self.cube['lastupdate'] = datetime.now()
        self.cube['run'] = True
        self.mongo['cube'].update({'slug': self.cube['slug']}, self.cube)

        log_it("CLEAN MEMORY: {}".format(self.slug), "bin-mining")
        gc.collect()


def process(_cube):
    try:
        log_it("START: {}".format(_cube['slug']), "bin-mining")

        mongo = MongoPlugin(
            uri=conf("mongodb")["uri"],
            db=conf("mongodb")["db"],
            json_mongo=True).get_mongo()

        MyClient = riak.RiakClient(
            protocol=conf("riak")["protocol"],
            http_port=conf("riak")["http_port"],
            host=conf("riak")["host"])

        MyBucket = MyClient.bucket(conf("riak")["bucket"])
        MyBucket.enable_search()

        c = CubeProcess(_cube)
        if _cube.get('type') == 'relational':
            c.load()
            c.frame()
            c.save()
        elif _cube.get('type') == 'cube_join':
            data = DataFrame({})
            fields = [rel['field']
                    for rel in _cube.get('relationship')]
            for i, rel in enumerate(_cube.get('relationship')):
                data = data.merge.concat(
                        DataFrame(MyBucket.get(rel['cube']).data),
                        keys=fields,
                        join='inner')

            c.environment(_cube.get('type'))
            c._data(data)
            c._keys(data.columns.values)
            c.frame()
            c.save()

    except Exception, e:
        log_it(e, "bin-mining")
        log_it(traceback.format_exc(), "bin-mining")
        _cube['run'] = False
        mongo['cube'].update({'slug': _cube['slug']}, _cube)

    log_it("END: {}".format(_cube['slug']), "bin-mining")


if __name__ == "__main__":
    run()
