#!/usr/bin/env python
# -*- coding: utf-8 -*-
import riak

import tornado.ioloop
import tornado.web
import tornado.gen

from utils import slugfy
from admin.forms import ConnectionForm, CubeForm


class CubeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, slug=None):
        form = CubeForm()
        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')

        get_bucket = myBucket.get('cube').data
        if get_bucket is None:
            get_bucket = []

        for bload in get_bucket:
            if bload['slug'] == slug:
                form.sql.data = bload['sql']
                form.conection.data = bload['conection']
                form.name.data = bload['name']

        self.render('admin/cube.html', form=form, cube=get_bucket)

    def post(self):
        form = CubeForm(self.request.arguments)
        if not form.validate():
            self.set_status(400)
            self.write(form.errors)

        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')

        data = form.data
        data['slug'] = slugfy(data.get('name'))

        get_bucket = myBucket.get('cube').data
        if get_bucket is None:
            get_bucket = []
        get_bucket.append(data)

        b1 = myBucket.new('cube', data=get_bucket)
        for k, v in data:
            b1.add_index(k, v)
        b1.store()

        self.redirect('/admin/cube')


class ConnectionHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        form = ConnectionForm()
        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')

        get_bucket = myBucket.get('connection').data
        if get_bucket is None:
            get_bucket = []

        self.render('admin/connection.html', form=form, connection=get_bucket)

    def post(self):
        form = ConnectionForm(self.request.arguments)
        if not form.validate():
            self.set_status(400)
            self.write(form.errors)

        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')

        data = form.data
        data['slug'] = slugfy(data.get('name'))

        get_bucket = myBucket.get('connection').data
        if get_bucket is None:
            get_bucket = []
        get_bucket.append(data)

        b1 = myBucket.new('connection', data=get_bucket)
        for k, v in data:
            b1.add_index(k, v)
        b1.store()

        self.redirect('/admin/connection')
