#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import MainHandler, ProcessHandler, DashboardHandler
from .views import ProcessWebSocket


INCLUDE_URLS = [
    (r"/process/(?P<slug>[\w-]+).ws", ProcessWebSocket),
    (r"/process/(?P<slug>[\w-]+).json", ProcessHandler),
    (r"/dashboard/(?P<slug>[\w-]+)", DashboardHandler),
    (r"/", MainHandler),
]
