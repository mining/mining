# -*- coding: utf-8 -*-
import gc
import pandas
from datetime import datetime

from pandas import DataFrame

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

from mining.utils import conf, log_it
from mining.utils._pandas import fix_render
from mining.db import DataWarehouse

from bottle.ext.mongo import MongoPlugin


class Cube(object):
    def __init__(self, _cube):

        log_it("START: {}".format(_cube['slug']), "bin-mining")

        self.mongo = MongoPlugin(
            uri=conf("mongodb")["uri"],
            db=conf("mongodb")["db"],
            json_mongo=True).get_mongo()

        try:
            del _cube['_id']
        except KeyError:
            pass
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
        if 'sqlite' in self.connection:
            e = create_engine(self.connection)
        else:
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

    def frame(self, data_type=None):
        log_it("LOAD DATA ON DATAWAREHOUSE via {}: {}".format(
            data_type or 'dict', self.slug), "bin-mining")
        if data_type:
            self.df = getattr(pandas, "read_{}".format(data_type))(self.data)
        else:
            self.df = DataFrame(self.data)

        if self.df.empty:
            self.pdict = {}
            log_it('[warning]Empty cube: {}!!'.format(self.cube),
                   "bin-mining")
            return

        try:
            self.df.columns = self.keys
        except AttributeError:
            self._keys(self.df.columns.tolist())

        # If the OML is active, it renders the script that there is
        if conf("oml").get("on") and self.cube.get("oml"):
            from oml import RunTime
            self.df.columns = self.keys
            df = RunTime(conf("oml").get("language", "lua"),
                         self.df.to_dict(orient='records'),
                         self.cube.get("oml"),
                         conf("oml").get("class", {"OML": "oml.base.OMLBase"}))
            self.df = DataFrame(df)
            self._keys(self.df.columns.tolist())

        self.df.head()
        self.pdict = map(fix_render, self.df.to_dict(orient='records'))

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
