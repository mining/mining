#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import APIDashboardHandler


INCLUDE_URLS = [
    (r"/api/dashboard.json", APIDashboardHandler),
]
