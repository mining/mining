#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from tornado.options import options

from mining.urls import INCLUDE_URLS as MINING_URLS
from admin.urls import INCLUDE_URLS as ADMIN_URLS


CORE = [(r'/assets/(.*)', tornado.web.StaticFileHandler,
         {'path': "{}/{}".format(options.PROJECT_PATH, "assets")})]

URLS = CORE + ADMIN_URLS + MINING_URLS
