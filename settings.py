#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))

#riak settings
RIAK_PROTOCOL = 'http'
RIAK_HTTP_PORT = 8098
RIAK_HOST = '127.0.0.1'

ADMIN_BUCKET_NAME = 'openminig-admin'
MINING_BUCKET_NAME = 'openmining'

#memcache settings
MEMCACHE_CONNECTION = '127.0.0.1:11211'
MEMCACHE_DEBUG = 0
