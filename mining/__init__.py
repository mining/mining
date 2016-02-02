#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pkg_resources


pkg_resources.declare_namespace(__name__)
VERSION = (0, 2, 2)

__version__ = ".".join(map(str, VERSION))
__status__ = "Alpha"
__description__ = "BI Application Server written by Python and Riak"
__author__ = "Thiago Avelino <thiago@avelino.xxx>"
__email__ = "thiago@avelino.xxx"
__license__ = "MIT License"
__copyright__ = "Copyright 2013, Open Mining"
