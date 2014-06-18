#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import json
import gc
import traceback
from datetime import datetime

from pandas import DataFrame

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

from mining.utils import conf, log_it
from mining.utils._pandas import fix_render, CubeJoin
from mining.multithread import ThreadPool
from mining.db.datawarehouse import DataWarehouse

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

        del _cube['_id']
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

        self.connection = self.mongo['connection'].find_one({
            'slug': self.cube['connection']})['connection']

        log_it("CONNECT IN RELATION DATA BASE: {}".format(self.slug),
               "bin-mining")
        e = create_engine(self.connection,
                          **conf('openmining')['sql_conn_params'])
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
        if type(keys) == list:
            self.keys = keys
        self.keys = list(keys)

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

    def save(self):
        log_it("SAVE DATA (JSON) ON DATA WAREHOUSE: {}".format(self.slug),
               "bin-mining")
        data = {'data': self.pdict, 'columns': self.keys}
        DW = DataWarehouse()
        DW.save(self.slug, data)

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

        c = CubeProcess(_cube)
        if _cube.get('type') == 'relational':
            c.load()
            c.frame()
            c.save()
        elif _cube.get('type') == 'cube_join':
            c.environment(_cube.get('type'))
            cube_join = CubeJoin(_cube)
            c._data(cube_join.none())
            c._keys(cube_join.none().columns.values)
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
