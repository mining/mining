#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import riak
import memcache
import functools

import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.autoreload

from tornado.websocket import WebSocketHandler

from pandas import DataFrame

from .utils import df_generate
from .models import MyBucket, MyAdminBucket


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        dashboard = MyAdminBucket.get('dashboard').data

        self.render('index.html', dashboard=dashboard or [])


class DashboardHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, slug):

        get_bucket = MyAdminBucket.get('dashboard').data

        elements = {}
        for d in get_bucket:
            if d['slug'] == slug:
                elements['slug'] = slug

                # GET ELEMENT
                _e = []
                for dash_element in d['element']:
                    element = MyAdminBucket.get('element').data
                    for e in element:
                        if dash_element == e['slug']:
                            try:
                                e['_type'] = e['type'].split('_')[1]
                            except:
                                e['_type'] = None
                            _e.append(e)
                    elements = _e

        self.render('dashboard.html', elements=elements, dashboard=get_bucket)


class ProcessWebSocketHandler(WebSocketHandler):
    def _queue(self, _send, _type):
        self.write_message(json.dumps({'type': _type, 'json': _send}))

    @tornado.web.asynchronous
    @tornado.gen.engine
    def open(self, slug):

        columns = json.loads(MyBucket.get('{}-columns'.format(slug)).data)
        fields = columns
        if self.get_argument('fields', None):
            fields = self.get_argument('fields').split(',')

        filters = [i[0] for i in self.request.arguments.iteritems()
                   if len(i[0].split('filter__')) > 1]

        df = DataFrame(MyBucket.get(slug).data, columns=fields)
        if len(filters) >= 1:
            for f in filters:
                df = df.query(df_generate(df, self.get_argument, f))

        self._queue(_type=u'columns', _send=fields)
        while True:
            map(functools.partial(_type=u'series'),
                df.to_dict(outtype='records'))


class ProcessHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self, slug):
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)

        columns = json.loads(MyBucket.get('{}-columns'.format(slug)).data)
        fields = columns
        if self.get_argument('fields', None):
            fields = self.get_argument('fields').split(',')

        filters = [i[0] for i in self.request.arguments.iteritems()
                   if len(i[0].split('filter__')) > 1]

        fields_json = json.dumps(fields)
        filters_json = json.dumps({f: self.get_argument(f) for f in filters})
        if mc.get(str(slug)) and\
                mc.get('{}-columns'.format(slug)) == fields_json and\
                mc.get('{}-fulters'.format(slug)) == filters_json:
            self.write(mc.get(str(slug)))
            self.finish()

        mc.set('{}-columns'.format(slug), fields_json)
        mc.set('{}-filters'.format(slug), filters_json)

        df = DataFrame(MyBucket.get(slug).data, columns=fields)
        if len(filters) >= 1:
            for f in filters:
                df = df.query(df_generate(df, self.get_argument, f))
        convert = df.to_dict(outtype='records')

        write = json.dumps({'columns': fields, 'json': convert})
        mc.set(str(slug), write)
        self.write(write)
        self.finish()
