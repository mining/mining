# -*- coding: utf-8 -*-
from mining.utils import conf, __from__


DW = __from__(conf('datawarehouse')['engine'])


class DataWarehouse(DW):
    pass
