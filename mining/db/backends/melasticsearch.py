# -*- coding: utf-8 -*-
import json
import requests
from bottle import request
from elasticsearch import Elasticsearch as ES

from mining.utils.listc import listc_dict


class Elasticsearch(object):

    _search = True

    def conn(self):
        """Open connection on Elasticsearch DataBase"""
        conn = ES([
            {"host": self.conf.get('host'),
             "port": self.conf.get('port')}
        ])
        return conn

    def save(self, house, data, content_type='dict'):
        """Save meta dada on Elasticsearch"""
        requests.delete("http://{}:{}/{}".format(
            self.conf.get('host'), self.conf.get('port'), house))
        for obj in data.get('data'):
            self.conn().index(index=house,
                              doc_type='data'.format(house),
                              body=obj)
        self.conn().index(index=house,
                          doc_type='columns',
                          body={"columns": data.get('columns')})
        return self.conn()

    def get(self, house, content_type="dict", callback={}):
        """Get meta data on Elasticsearch"""
        count = self.conn().count(index=house, doc_type="data").get('count')
        doc_data = self.conn().search(index=house, doc_type='data',
                                      body=self.filter(), size=count)
        data = {}
        """
        data['data'] = [obj.get("_source")
                        for obj in doc_data.get('hits').get('hits')]
        """
        data['data'] = listc_dict(doc_data.get('hits').get('hits'), "_source")
        doc_columns = self.conn().search(index=house, doc_type='columns',
                                         body=self.filter())
        data.update(doc_columns.get('hits').get('hits')[0].get('_source'))
        data['count'] = count
        return data

    def filter(self):
        """Generate dict to applay filter on Elasticsearch"""
        filter = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"country": "Brazil"}},
                        {"match": {"full_name": "Daniel Austin"}}
                    ]
                }
            }
        }
        filter = {"query": {"match_all": {}}}
        return filter
