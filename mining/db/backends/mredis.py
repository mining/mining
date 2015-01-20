#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from redis import StrictRedis
from mining.db.datawarehouse import GenericDataWarehouse


class Redis(GenericDataWarehouse):

    search = False

    def conn(self):
        """Open connection on Redis DataBase"""
        conn = StrictRedis(host=self.conf.get('host'),
                           port=self.conf.get('port'),
                           db=int(self.conf.get('db')))
        return conn

    def save(self, house, data, content_type="application/json"):
        """Save meta dada on Redis"""
        if content_type == "application/json":
            return self.conn().set(house, json.dumps(data))
        return self.conn().set(house, data)

    def get(self, house, content_type="application/json", callback={},
            filters=[], page=1):
        """Get bucket"""
        if content_type == "application/json":
            return json.loads(self.conn().get(house)) or callback
        return self.conn().get(house) or callback
