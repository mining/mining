#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import Dashboard, CubeQuery, Connection, Cube, Element


INCLUDE_URLS = [
    (r"/api/dashboard/", Dashboard),
    (r"/api/dashboard/(?P<slug>[\w-]+)", Dashboard),

    (r"/api/connection/", Connection),
    (r"/api/connection/(?P<slug>[\w-]+)", Connection),

    (r"/api/cube/", Cube),
    (r"/api/cube/(?P<slug>[\w-]+)", Cube),

    (r"/api/element/", Element),
    (r"/api/element/(?P<slug>[\w-]+)", Element),

    (r"/api/cubequery.json", CubeQuery),
]
