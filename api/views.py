#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import tornado.web

from admin.models import MyAdminBucket


class APIDashboardHandler(tornado.web.RequestHandler):
    def get(self):
        get_bucket = MyAdminBucket.get('dashboard').data
        if get_bucket is None:
            get_bucket = []

        self.write(json.dumps(get_bucket))
        self.finish()
