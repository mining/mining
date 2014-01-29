#!/usr/bin/env python
# -*- coding: utf-8 -*-
import riak

import tornado.ioloop
import tornado.web
import tornado.gen

from mining.utils import slugfy
from admin.forms import ConnectionForm, CubeForm, ElementForm, DashboardForm


class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/base.html')


class DashboardHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, slug=None):
        form = DashboardForm()
        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')

        get_bucket = myBucket.get('dashboard').data
        if get_bucket is None:
            get_bucket = []

        for bload in get_bucket:
            if bload['slug'] == slug:
                for k in form._fields:
                    getattr(form, k).data = bload[k]

        self.render('admin/dashboard.html',
                    form=form,
                    dashboard=get_bucket,
                    slug=slug)

    def post(self, slug=None):
        form = DashboardForm(self.request.arguments)
        if not form.validate():
            self.set_status(400)
            self.write(form.errors)

        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')

        data = form.data
        data['slug'] = slugfy(data.get('name'))

        get_bucket = [b for b in myBucket.get('dashboard').data or []
                      if b['slug'] != data['slug']]
        if get_bucket is None:
            get_bucket = []
        get_bucket.append(data)

        b1 = myBucket.new('dashboard', data=get_bucket)
        """
        for k in data:
            b1.add_index("{}_bin".format(k), data[k])
        """
        b1.store()

        self.redirect('/admin/dashboard')


class ElementHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, slug=None):
        form = ElementForm()
        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')

        get_bucket = myBucket.get('element').data
        if get_bucket is None:
            get_bucket = []

        for bload in get_bucket:
            if bload['slug'] == slug:
                for k in form._fields:
                    getattr(form, k).data = bload[k]

        self.render('admin/element.html',
                    form=form,
                    element=get_bucket,
                    slug=slug)

    def post(self, slug=None):
        form = ElementForm(self.request.arguments)
        if not form.validate():
            self.set_status(400)
            self.write(form.errors)

        myClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')
        myBucket = myClient.bucket('openmining-admin')

        data = form.data
        data['slug'] = slugfy(data.get('name'))

        get_bucket = [b for b in myBucket.get('element').data or []
                      if b['slug'] != data['slug']]
        if get_bucket is None:
            get_bucket = []
        get_bucket.append(data)

        b1 = myBucket.new('element', data=get_bucket)
        for k in data:
            b1.add_index("{}_bin".format(k), data[k])
        b1.store()

        self.redirect('/admin/element')


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
                for k in form._fields:
                    getattr(form, k).data = bload[k]

        self.render('admin/cube.html', form=form, cube=get_bucket, slug=slug)

    def post(self, slug=None):
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

        get_bucket = [b for b in myBucket.get('cube').data or []
                      if b['slug'] != data['slug']]
        if get_bucket is None:
            get_bucket = []
        get_bucket.append(data)

        b1 = myBucket.new('cube', data=get_bucket)
        for k in data:
            b1.add_index("{}_bin".format(k), data[k])
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
        b1.store()

        self.redirect('/admin/connection')
