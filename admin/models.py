#!/usr/bin/env python
# -*- coding: utf-8 -*-
import riak


MyClient = riak.RiakClient(protocol='http',
                                   http_port=8098,
                                   host='127.0.0.1')

MyBucket = MyClient.bucket('openmining-admin')


def main():
    pass

if __name__ == '__main__':
    main()
