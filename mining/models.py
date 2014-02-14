#!/usr/bin/env python
# -*- coding: utf-8 -*-
import riak


MyClient = riak.RiakClient(protocol='http',
                           http_port=8098,
                           host='127.0.0.1')

MyAdminBucket = MyClient.bucket('openmining-admin')
MyBucket = MyClient.bucket('openmining')


def main():
    pass

if __name__ == '__main__':
    main()
