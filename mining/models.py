#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import riak

#hacking for import global settings
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_DIR)

from settings import (RIAK_PROTOCOL, RIAK_HTTP_PORT,
                      RIAK_HOST, ADMIN_BUCKET_NAME,
                      MINING_BUCKET_NAME, MEMCACHE_CONNECTION, MEMCACHE_DEBUG)


MyClient = riak.RiakClient(protocol=RIAK_PROTOCOL,
                           http_port=RIAK_HTTP_PORT,
                           host=RIAK_HOST)

MyAdminBucket = MyClient.bucket(ADMIN_BUCKET_NAME)

MyBucket = MyClient.bucket(MINING_BUCKET_NAME)


def main():
    pass

if __name__ == '__main__':
    main()
