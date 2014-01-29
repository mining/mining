#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import AdminHandler, CubeHandler, ConnectionHandler

INCLUDE_URLS = [
    (r"/admin", AdminHandler),
    (r"/admin/connection", ConnectionHandler),
    (r"/admin/cube/?(?P<slug>[\w-]+)?", CubeHandler),
]
