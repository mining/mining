# -*- coding: utf-8 -*-
import json
from elasticsearch import Elasticsearch as ES


class Elasticsearch(object):
    def conn(self):
        """Open connection on Elasticsearch DataBase"""
        conn = ES([
            {"host": self.conf.get('host'),
             "port": self.conf.get('port'),
             "url_prefix": self.conf.get('db')}
        ])
        return conn

    def save(self, house, data, content_type=None):
        """Save meta dada on Elasticsearch"""
        if content_type == "application/json":
            data = json.dumps(data)
        return self.conn().index(index=house, doc_type='json', id=1,
                                 body=data)

    def get(self, house, content_type="application/json", callback={}):
        """Get meta data on Elasticsearch"""
        data = self.conn().get(index=house, doc_type='json', id=1) or callback
        if content_type == "application/json":
            return json.loads(data['_source'])
        return data['_source']
