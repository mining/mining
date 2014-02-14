#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import MainHandler, ProcessHandler, DashboardHandler


INCLUDE_URLS = [
    (r"/process/(?P<slug>[\w-]+).json", ProcessHandler),
    (r"/dashboard/(?P<slug>[\w-]+)", DashboardHandler),
    (r"/", MainHandler),
]
