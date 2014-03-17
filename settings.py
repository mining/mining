#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'views')
STATIC_PATH = os.path.join(PROJECT_PATH, 'assets')

# Open Mining
MINING_PORT = 8888
MINING_IP = u'0.0.0.0'

# Riak
RIAK_PROTOCOL = 'http'
RIAK_HTTP_PORT = 8098
RIAK_HOST = u'127.0.0.1'

ADMIN_BUCKET_NAME = u'openminig-admin'
MINING_BUCKET_NAME = u'openmining'

# Memcache
MEMCACHE_CONNECTION = u'127.0.0.1:11211'
MEMCACHE_DEBUG = 0

# MongoDB
MONGO_URI = 'mongodb://127.0.0.1'
