#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import AdminHandler, CubeHandler, ConnectionHandler
from .views import ElementHandler


INCLUDE_URLS = [
    (r"/admin", AdminHandler),
    (r"/admin/connection", ConnectionHandler),
    (r"/admin/cube/?(?P<slug>[\w-]+)?", CubeHandler),
    (r"/admin/element/?(?P<slug>[\w-]+)?", ElementHandler),
]
