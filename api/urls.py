#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import APIDashboardHandler, CubeQuery


INCLUDE_URLS = [
    (r"/api/dashboard.json", APIDashboardHandler),
    (r"/api/cubequery.json", CubeQuery),
]
