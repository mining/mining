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

    def get(self, house, filters=None, content_type="dict", callback={}):
        """Get meta data on Elasticsearch"""
        count = self.conn().count(index=house, doc_type="data").get('count')
        doc_data = self.conn().search(index=house, doc_type='data',
                                      body=self.filter(filters=filters),
                                      size=count)
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

    def filter(self, filters=[]):
        """Generate dict to applay filter on Elasticsearch
        should: OR
        must: AND
        """
        filter = {
            "query": {
                "filtered": {
                    "query": {
                        "bool": {
                            "must": []
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": []
                        }
                    }
                }
            }
        }
        filtered_query = filter['query']["filtered"]["query"]['bool']['must']
        filtered_filter = filter['query']["filtered"]["filter"]['bool']['must']

        if len(filters) >= 1:
            for f in filters:
                s = f.split('__')
                field = s[1]
                operator = s[2]
                value = request.GET.get(f)
                if operator == 'is':
                    filter_type = "match"
                    filter_obj = filtered_query
                    if len(value.split(" ")) == 1:
                        filter_type = "term"
                        filter_obj = filtered_filter
                        if type(value) in [str, unicode]:
                            value = value.lower()

                    filter_obj.append({filter_type: {field: value}})
                """
                if operator == 'like':
                    df = df[df[field].str.contains(value)]
                elif operator == 'regex':
                    df = DataFrameSearchColumn(df, field, value, operator)
                else:
                    df = df.query(df_generate(df, value, f))
                """
            return filter
        return {"query": {"match_all": {}}}
