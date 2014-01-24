#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

import riak
import memcache

import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.autoreload

from pandas import read_json
from utils import pandas_to_dict


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('index.html')


class ProcessHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        if mc.get('testando'):
            self.write(mc.get('testando'))
            self.finish()

        myClient = riak.RiakClient(protocol='http', http_port=8098, host='127.0.0.1')
        myBucket = myClient.bucket('openmining')

        columns = json.loads(myBucket.get('testando-columns').data)
        df = read_json(myBucket.get('testando').data)

        fields = columns
        try:
            if len(self.get_argument('fields')) >= 1:
                fields = self.get_argument('fields').split(',')
        except:
            pass
        fields.remove('pedido_data')
        fields.remove('cliente_data')

        df[fields].head()

        convert = pandas_to_dict(df)

        write = json.dumps({'columns': columns, 'json': convert})
        mc.set('testando', write)
        self.write(write)
        self.finish()


PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))
application = tornado.web.Application([
    (r'/assets/(.*)', tornado.web.StaticFileHandler,
        {'path': "{}/{}".format(PROJECT_PATH, "assets")}),
    (r"/process.json", ProcessHandler),
    (r"/", MainHandler),
])


if __name__ == "__main__":
    print "openmining.io server starting..."
    def fn():
        print "openmining.io before reloading..."
    application.listen(8888)
    tornado.autoreload.add_reload_hook(fn)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
