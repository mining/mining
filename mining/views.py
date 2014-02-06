#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import riak
import memcache
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.autoreload

from pandas import read_json

from .utils import pandas_to_dict, df_generate


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')
        dashboard = myBucket.get('dashboard').data

        self.render('index.html', dashboard=dashboard)


class DashboardHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, slug):

        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')
        get_bucket = myBucket.get('dashboard').data

        dashboard = {}
        for d in get_bucket:
            if d['slug'] == slug:
                dashboard['slug'] = slug

                # GET ELEMENT
                _e = []
                for dash_element in d['element']:
                    element = myBucket.get('element').data
                    for e in element:
                        if dash_element == e['slug']:
                            try:
                                e['_type'] = e['type'].split('_')[1]
                            except:
                                e['_type'] = None
                            _e.append(e)
                    dashboard = _e

        self.render('dashboard.html', dashboard=dashboard)


class ProcessHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self, slug):
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining')

        columns = json.loads(myBucket.get('{}-columns'.format(slug)).data)
        fields = columns
        if self.get_argument('fields', None):
            fields = self.get_argument('fields').split(',')

        fields_json = json.dumps(fields)
        if mc.get(str(slug)) and\
                mc.get('{}-columns'.format(slug)) == fields_json:
            #self.write(mc.get(str(slug)))
            #self.finish()
            pass

        mc.set('{}-columns'.format(slug), fields_json)

        df = read_json(myBucket.get(slug).data)

        filters = [i[0] for i in self.request.arguments.iteritems()
                   if len(i[0].split('filter__')) > 1]

        read = df[fields]
        if len(filters) >= 1:
            test = ()
            for f in filters:
                test = df_generate(df, self.get_argument, f)
            read = df[test]
        convert = pandas_to_dict(read)

        write = json.dumps({'columns': fields, 'json': convert})
        mc.set(str(slug), write)
        self.write(write)
        self.finish()
