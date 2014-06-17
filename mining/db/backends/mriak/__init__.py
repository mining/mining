#!/usr/bin/env python
# -*- coding: utf-8 -*-
from riak import RiakClient


class Riak(object):
    def conn(self):
        """Open connection on Riak DataBase"""
        client = RiakClient(
            protocol=self.conf.get("protocol"),
            http_port=self.conf.get("port"),
            host=self.conf.get("host"))

        conn = client.bucket(self.conf.get("db"))
        conn.enable_search()
        return conn

    def save(self, house, data, content_type="application/json"):
        """Save meta dada on Riak"""
        return self.conn().new(house, data=data,
                               content_type=content_type).store()

    def get(self, house, callback={}):
        """Get bucket"""
        return self.conn().get(house).data or callback
