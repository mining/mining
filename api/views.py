#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import tornado.web
import riak

from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from settings import (RIAK_PROTOCOL, RIAK_HTTP_PORT,
                      RIAK_HOST, ADMIN_BUCKET_NAME,
                      MINING_BUCKET_NAME, MEMCACHE_CONNECTION, MEMCACHE_DEBUG)
from admin.models import MyAdminBucket


class APIDashboardHandler(tornado.web.RequestHandler):
    def get(self):
        get_bucket = MyAdminBucket.get('dashboard').data
        if get_bucket is None:
            get_bucket = []

        self.write(json.dumps(get_bucket))
        self.finish()


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
