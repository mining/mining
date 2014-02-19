#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from datetime import date, datetime
from decimal import Decimal
from pandas import tslib, DataFrame

from utils import slugfy, fix_type, fix_render, df_generate


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


class fix_render_test(unittest.TestCase):
    def test_render_dict(self):
        data = [{'h': 1, 'v': 'a'}, {'h': 1, 'v': 'a'}]
        for d in data:
            self.assertEquals(fix_render(d), {'h': 1, 'v': u'a'})


class df_generate_test(unittest.TestCase):
    def test_between_date(self):
        df = DataFrame([{'date': '2014-01-01'},
                        {'date': '2014-02-01'},
                        {'date': '2014-03-01'}])
        g = df_generate(df, "2014-01-01:2014-02-01",
                        "filter__date__between__date__:Y-:m-:d")

        self.assertEquals(g, u"date in ['2014-01-01', '2014-01-02', "
                          "'2014-01-03', '2014-01-04', '2014-01-05', "
                          "'2014-01-06', '2014-01-07', '2014-01-08', "
                          "'2014-01-09', '2014-01-10', '2014-01-11', "
                          "'2014-01-12', '2014-01-13', '2014-01-14', "
                          "'2014-01-15', '2014-01-16', '2014-01-17', "
                          "'2014-01-18', '2014-01-19', '2014-01-20', "
                          "'2014-01-21', '2014-01-22', '2014-01-23', "
                          "'2014-01-24', '2014-01-25', '2014-01-26', "
                          "'2014-01-27', '2014-01-28', '2014-01-29', "
                          "'2014-01-30', '2014-01-31', '2014-02-01']")
