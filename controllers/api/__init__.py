#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle

from .connection import connection_app


ADMIN_BUCKET_NAME = 'openminig-admin'

api_app = Bottle()
api_app.mount('/connection', connection_app)


@api_app.route('/')
def index():
    return 'OpenMining API!'
