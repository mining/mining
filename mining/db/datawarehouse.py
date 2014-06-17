#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mining.utils import conf


try:
    _import = conf('datawarehouse')['engine'].split('.')[-1]
    _from = u".".join(conf('datawarehouse')['engine'].split('.')[:-1])
    DW = getattr(__import__(_from, fromlist=[_import]), _import)
except:
    DW = object


class DataWarehouse(DW):
    def __init__(self):
        self.conf = conf('datawarehouse')
