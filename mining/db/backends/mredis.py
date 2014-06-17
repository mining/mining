#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from redis import StrictRedis


class Redis(object):
    def conn(self):
        """Open connection on Riak DataBase"""
        conn = StrictRedis(host=self.conf.get('host'),
                           port=self.conf.get('port'),
                           db=int(self.conf.get('db')))
        return conn

    def save(self, house, data, content_type="application/json"):
        """Save meta dada on Riak"""
        return self.conn().set(house, json.dumps(data))

    def get(self, house, callback={}):
        """Get bucket"""
        return json.loads(self.conn().get(house)) or callback
