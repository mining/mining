#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import MainHandler, ProcessHandler, DashboardHandler
from .views import ProcessWebSocketHandler


INCLUDE_URLS = [
    (r"/process/(?P<slug>[\w-]+).ws", ProcessWebSocketHandler),
    (r"/process/(?P<slug>[\w-]+).json", ProcessHandler),
    (r"/process/(?P<slug>[\w-]+).json", ProcessHandler),
    (r"/(?P<slug>[\w-]+)", DashboardHandler),
    (r"/", MainHandler),
]
