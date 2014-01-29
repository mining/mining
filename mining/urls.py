#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import MainHandler, ProcessHandler


INCLUDE_URLS = [
    (r"/process/(?P<slug>[\w-]+).json", ProcessHandler),
    (r"/(?P<slug>[\w-]+)", MainHandler)]
