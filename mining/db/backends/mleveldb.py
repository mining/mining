#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from leveldb import LevelDB as DB
from mining.db.datawarehouse import GenericDataWarehouse


class LevelDB(GenericDataWarehouse):
    def conn(self):
        """Open connection on LevelDB DataBase"""
        conn = DB("/tmp/{}.mining".format(self.conf.get("db")))
        return conn

    def save(self, house, data, content_type="application/json"):
        """Save meta dada on LevelDB"""
        if content_type == "application/json":
            return self.conn().Put(house, json.dumps(data))
        return self.conn.Put(house, data)

    def get(self, house, content_type="application/json", callback={},
            filters=[], page=1):
        """Get bucket"""
        if content_type == "application/json":
            return json.loads(self.conn().Get(house)) or callback
        return self.conn.Get(house) or callback
