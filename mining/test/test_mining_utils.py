#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from datetime import date, datetime
from decimal import Decimal
from pandas import tslib, DataFrame

from mining.utils import slugfy
from mining.utils._pandas import fix_type, fix_render, df_generate


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
        data = [{'h': 1, 'v': 'a'}, {'h': 2, 'v': 'b'}]
        self.assertEquals(fix_render(data[0]), {'h': 1, 'v': u'a'})
        self.assertEquals(fix_render(data[1]), {'h': 2, 'v': u'b'})


class df_generate_test(unittest.TestCase):
    def setUp(self):
        self.df = DataFrame([
            {'date': '2014-01-01', 'int': 1, 'str': 'Angular'},
            {'date': '2014-02-01', 'int': 2, 'str': 'Credit'},
            {'date': '2014-03-01', 'int': 3, 'str': 'Diamon'}])


class df_generate_between_test(df_generate_test):
    def test_between_date(self):
        g = df_generate(self.df, "2014-01-01:2014-02-01",
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


class df_generate_in_test(df_generate_test):
    def test_in_str(self):
        g = df_generate(self.df, "1,2,3", "filter__int__in")
        self.assertEquals(g, u"int in ['1', '2', '3']")

    def test_in_str_text(self):
        g = df_generate(self.df, "Diamond,Angular", "filter__str__in__str")
        self.assertEquals(g, u"str in ['Diamond', 'Angular']")

    def test_in_int(self):
        g = df_generate(self.df, "1,2,3", "filter__int__in__int")
        self.assertEquals(g, u"int in [1, 2, 3]")


class df_generate_notin_test(df_generate_test):
    def test_notin_str(self):
        g = df_generate(self.df, "1,2,3", "filter__int__notin")
        self.assertEquals(g, u"['1', '2', '3'] not in int")

    def test_notin_int(self):
        g = df_generate(self.df, "1,2,3", "filter__int__notin__int")
        self.assertEquals(g, u"[1, 2, 3] not in int")


class df_generate_is_test(df_generate_test):
    def test_is(self):
        g = df_generate(self.df, "2014-01-01", "filter__date")
        self.assertEquals(g, u"date == '2014-01-01'")

    def test_is_type_str_text(self):
        g = df_generate(self.df, "Diamon", "filter__nivel__is__str")
        self.assertEquals(g, u"nivel == 'Diamon'")

    def test_is_type_int(self):
        g = df_generate(self.df, "1", "filter__int__is__int")
        self.assertEquals(g, u"int == 1")

    def test_is_type_str(self):
        g = df_generate(self.df, "1", "filter__int__is__str")
        self.assertEquals(g, u"int == '1'")


class df_generate_gte_test(df_generate_test):
    def test_gte(self):
        g = df_generate(self.df, "1", "filter__int__gte")
        self.assertEquals(g, u"int >= 1")


class df_generate_lte_test(df_generate_test):
    def test_lte(self):
        g = df_generate(self.df, "1", "filter__int__lte")
        self.assertEquals(g, u"int <= 1")
