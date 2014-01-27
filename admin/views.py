#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.gen


class CubeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('index.html')
