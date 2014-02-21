#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import MainHandler, ProcessHandler, DashboardHandler
from .views import ProcessWebSocket, ExportHandler


INCLUDE_URLS = [
    (r"/process/(?P<slug>[\w-]+).ws", ProcessWebSocket),
    (r"/process/(?P<slug>[\w-]+).json", ProcessHandler),
    (r"/process/(?P<slug>[\w-]+).(?P<ext>[\w-]+)", ExportHandler),
    (r"/dashboard/(?P<slug>[\w-]+)", DashboardHandler),
    (r"/", MainHandler),
]
