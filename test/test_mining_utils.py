#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

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
