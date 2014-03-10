#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import tornado.ioloop
import tornado.web
import tornado.gen

from redis import Redis
from rq import Queue

from settings import MINING_BUCKET_NAME
from utils import slugfy
from admin.forms import ConnectionForm, CubeForm, ElementForm, DashboardForm
from admin.forms import ObjGenerate
from admin.models import MyAdminBucket, MyClient


class APIElementCubeHandler(tornado.web.RequestHandler):
    def get(self, slug):
        MyBucket = MyClient.bucket(MINING_BUCKET_NAME)
        data = MyBucket.get(u'{}-columns'.format(slug)).data or '{}'
        columns = json.loads(data)

        self.write({'columns': columns})
        self.finish()


class DashboardHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, slug=None):
        form = DashboardForm()
        form.element.choices = ObjGenerate('element', 'slug', 'name')

        get_bucket = MyAdminBucket.get('dashboard').data
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

        data = form.data
        data['slug'] = slugfy(data.get('name'))

        get_bucket = [b for b in MyAdminBucket.get('dashboard').data or []
                      if b['slug'] != data['slug']]
        if get_bucket is None:
            get_bucket = []
        get_bucket.append(data)

        b1 = MyAdminBucket.new('dashboard', data=get_bucket)
        MyAdminBucket.clear_properties()
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
        form.cube.choices = ObjGenerate('cube', 'slug', 'name')

        get_bucket = MyAdminBucket.get('element').data
        if get_bucket is None:
            get_bucket = []

        categorie = None
        for bload in get_bucket:
            if bload['slug'] == slug:
                for k in form._fields:
                    getattr(form, k).data = bload[k]
                categorie = bload.get('categories')

        self.render('admin/element.html',
                    form=form,
                    element=get_bucket,
                    categorie=categorie,
                    slug=slug)

    def post(self, slug=None):
        form = ElementForm(self.request.arguments)
        if not form.validate():
            self.set_status(400)
            self.write(form.errors)

        data = form.data
        data['slug'] = slugfy(data.get('name'))
        data['categories'] = self.request.arguments.get('categories')[0]

        get_bucket = [b for b in MyAdminBucket.get('element').data or []
                      if b['slug'] != data['slug']]
        if get_bucket is None:
            get_bucket = []
        get_bucket.append(data)

        b1 = MyAdminBucket.new('element', data=get_bucket)
        b1.add_index("slug_bin", data['slug'])
        b1.add_index("type_bin", data['type'])
        b1.add_index("cube_bin", data['cube'])
        b1.store()
        MyAdminBucket.clear_properties()

        self.redirect('/admin/element')


class CubeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, slug=None):
        form = CubeForm()
        form.connection.choices = ObjGenerate('connection', 'slug', 'name')

        get_bucket = MyAdminBucket.get('cube').data or []

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

        data = form.data
        data['slug'] = slugfy(data.get('name'))
        data['sql'] = data.get('sql').replace("\n", "").replace("\r", "")
        data['sql'] = data.get('sql').replace("\t", " ")

        get_bucket = [b for b in MyAdminBucket.get('cube').data or []
                      if b['slug'] != data['slug']]
        if get_bucket is None:
            get_bucket = []
        get_bucket.append(data)

        b1 = MyAdminBucket.new('cube', data=get_bucket)
        b1.add_index("slug_bin", data['slug'])
        b1.add_index("connection_bin", data['connection'])
        b1.store()
        MyAdminBucket.clear_properties()

        Queue(connection=Redis()).enqueue_call(
            func='bin.mining.run',
            args=(slug,)
        )

        self.redirect('/admin/cube')


class ConnectionHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, slug=None):
        form = ConnectionForm()

        get_bucket = MyAdminBucket.get('connection').data or []

        for bload in get_bucket:
            if bload['slug'] == slug:
                for k in form._fields:
                    getattr(form, k).data = bload[k]

        self.render('admin/connection.html', form=form, slug=slug,
                    connection=get_bucket)

    def post(self, slug=None):
        form = ConnectionForm(self.request.arguments)
        if not form.validate():
            self.set_status(400)
            self.write(form.errors)

        data = form.data
        data['slug'] = slugfy(data.get('name'))

        get_bucket = MyAdminBucket.get('connection').data or []
        get_bucket = [b for b in get_bucket if b['slug'] != data['slug']]

        if get_bucket is None:
            get_bucket = []
        get_bucket.append(data)

        b1 = MyAdminBucket.new('connection', data=get_bucket)
        b1.store()
        MyAdminBucket.clear_properties()

        self.redirect('/admin/connection')


class DeleteHandler(tornado.web.RequestHandler):
    def get(self, bucket, slug):
        get_bucket = MyAdminBucket.get(bucket).data or []

        value = None
        for i in get_bucket:
            if i.get(bucket) == slug:
                value = i.get(bucket)
        get_bucket = [b for b in get_bucket if b['slug'] != slug]

        MyAdminBucket.new(bucket, data=get_bucket).store()
        MyAdminBucket.clear_properties()

        Queue(connection=Redis()).enqueue_call(
            func='admin.tasks.related_delete',
            args=(bucket, slug, value)
        )

        self.redirect('/admin/{}'.format(bucket))
