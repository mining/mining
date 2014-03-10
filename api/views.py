#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import tornado.web
import riak

from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from redis import Redis
from rq import Queue

from settings import (RIAK_PROTOCOL, RIAK_HTTP_PORT,
                      RIAK_HOST, ADMIN_BUCKET_NAME,
                      MINING_BUCKET_NAME, MEMCACHE_CONNECTION, MEMCACHE_DEBUG)
from admin.models import MyAdminBucket
from utils import slugfy


class ApiHandler(tornado.web.RequestHandler):
    bucket = []

    @tornado.web.asynchronous
    def get(self, slug=None):
        bucket = MyAdminBucket.get(self.str_bucket).data or []
        my_bucket = MyAdminBucket.get(self.str_bucket)

        if slug:
            value = {}
            for i in bucket:
                if i.get('slug') == slug:
                    value = i
            bucket = value

        self.write(json.dumps(bucket))
        self.finish()

    def post(self):
        data = json.loads(self.request.body)
        data['slug'] = slugfy(data.get('name'))

        bucket = MyAdminBucket.get(self.str_bucket).data or []
        my_bucket = MyAdminBucket.get(self.str_bucket)

        bucket = [b for b in bucket if b['slug'] != data['slug']]
        bucket.append(data)

        MyAdminBucket.new(my_bucket.key, data=bucket).store()

        self.write("Post or Put ok!")
        self.finish()

    def put(self, slug=None):
        self.post()

    @tornado.web.asynchronous
    def delete(self, slug):
        bucket = MyAdminBucket.get(self.str_bucket).data or []
        my_bucket = MyAdminBucket.get(self.str_bucket)

        value = None
        for i in bucket:
            if i.get(my_bucket.key) == slug:
                value = i.get(my_bucket.key)
        new_bucket = [b for b in bucket if b['slug'] != slug]

        MyAdminBucket.new(my_bucket.key, data=new_bucket).store()

        Queue(connection=Redis()).enqueue_call(
            func='admin.tasks.related_delete',
            args=(my_bucket.key, slug, value)
        )

        self.write("Delete ok!")
        self.finish()


class Connection(ApiHandler):
    str_bucket = 'connection'


class Cube(ApiHandler):
    str_bucket = 'cube'


class Dashboard(ApiHandler):
    str_bucket = 'dashboard'


class Element(ApiHandler):
    str_bucket = 'element'


class CubeQuery(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        post = json.loads(self.request.body)

        MyClient = riak.RiakClient(protocol=RIAK_PROTOCOL,
                                   http_port=RIAK_HTTP_PORT,
                                   host=RIAK_HOST)

        MyAdminBucket = MyClient.bucket(ADMIN_BUCKET_NAME)

        connection = None
        for c in MyAdminBucket.get('connection').data:
            if c['slug'] == post.get('connection', None):
                connection = c['connection']

        sql = """SELECT * FROM ({}) AS CUBE LIMIT 10;""".format(
            post.get('sql', None))

        e = create_engine(connection)
        connection = e.connect()
        try:
            resoverall = connection.execute(text(sql))
        except:
            self.write({'sql': '', 'msg': 'Error!'})
            self.finish()

        df = DataFrame(resoverall.fetchall())
        if df.empty:
            self.finish()
        df.columns = resoverall.keys()
        df.head()

        self.write({'sql': df.to_json(orient='records'), 'msg': 'Success!'})
        self.finish()
