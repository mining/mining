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
from admin.views import CubeHandler, ConnectionHandler


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, slug):
        self.render('index.html', slug=slug)


class ProcessHandler(tornado.web.RequestHandler):
    def post(self, slug):
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining')

        columns = json.loads(myBucket.get('{}-columns'.format(slug)).data)
        fields = columns
        try:
            if len(self.get_argument('fields')) >= 1:
                fields = self.get_argument('fields').split(',')
        except:
            pass

        fields_json = json.dumps(fields)
        if mc.get(str(slug)) and\
                mc.get('{}-columns'.format(slug)) == fields_json:
            self.write(mc.get(slug))
            self.finish()

        mc.set('{}-columns'.format(slug), fields_json)

        df = read_json(myBucket.get(slug).data)

        read = df[fields]
        convert = pandas_to_dict(read)

        write = json.dumps({'columns': fields, 'json': convert})
        mc.set(str(slug), write)
        self.write(write)
        self.finish()


PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))
settings = dict(
    template_path="{}/{}".format(PROJECT_PATH, 'templates'))

application = tornado.web.Application([
    (r'/assets/(.*)', tornado.web.StaticFileHandler,
        {'path': "{}/{}".format(PROJECT_PATH, "assets")}),
    (r"/admin/connection", ConnectionHandler),
    (r"/admin/cube/?(?P<slug>[\w-]+)?", CubeHandler),
    (r"/process/(?P<slug>[\w-]+).json", ProcessHandler),
    (r"/?(?P<slug>[\w-]+)?", MainHandler),
], **settings)


if __name__ == "__main__":
    print "openmining.io server starting..."

    def fn():
        print "openmining.io before reloading..."

    application.listen(8888)
    tornado.autoreload.add_reload_hook(fn)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
