#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from datetime import date, datetime
from decimal import Decimal
from pandas import tslib

from mining.utils import slugfy, fix_type


class df_slugfy_test(unittest.TestCase):
    def test_generate_simples(self):
        self.assertEquals(u"testamdo-slugfy", slugfy(u"Testamdo slugfy"))

    def test_used_accents(self):
        self.assertEquals(u"testando-se-e-slugfy",
                          slugfy(u"Testando sé é slugfy"))


class fix_type_test(unittest.TestCase):
    def test_str_latin1(self):
        self.assertEquals(fix_type("test".encode('latin1')), u"test")
        self.assertEqual(type(fix_type("test".encode("latin1"))), unicode)

    def test_str(self):
        self.assertEquals(fix_type("test"), u"test")
        self.assertEqual(type(fix_type("test")), unicode)

    def test_timestamp(self):
        t = tslib.Timestamp.now()
        self.assertEquals(fix_type(t), t.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEquals(type(fix_type(t)), str)

    def test_datetime(self):
        d = datetime.now()
        self.assertEquals(fix_type(d), d.strftime("%Y-%m-%d"))
        self.assertEquals(type(fix_type(d)), str)

    def test_date(self):
        d = date.today()
        self.assertEquals(fix_type(d), d.strftime("%Y-%m-%d"))
        self.assertEquals(type(fix_type(d)), str)

    def test_decimal(self):
        d = Decimal(10.10)
        self.assertEquals(fix_type(d), float(10.1))
        self.assertEquals(type(fix_type(d)), float)
