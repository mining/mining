#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import CubeHandler, ConnectionHandler
from .views import ElementHandler, DashboardHandler, APIElementCubeHandler


INCLUDE_URLS = [
    (r"/admin/connection/?(?P<slug>[\w-]+)?", ConnectionHandler),
    (r"/admin/cube/?(?P<slug>[\w-]+)?", CubeHandler),
    (r"/admin/api/element/cube/?(?P<slug>[\w-]+)?", APIElementCubeHandler),
    (r"/admin/element/?(?P<slug>[\w-]+)?", ElementHandler),
    (r"/admin/dashboard/?(?P<slug>[\w-]+)?", DashboardHandler),
]
