# -*- coding: utf-8 -*-
from mining.utils import conf


class GenericDataWarehouse(object):
    def __init__(self):
        self.conf = conf('datawarehouse')
        self.search = False
