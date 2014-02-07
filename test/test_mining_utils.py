#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from mining.utils import slugfy


class df_slugfy_test(unittest.TestCase):
    def test_generate_simples(self):
        self.assertEquals(u"testamdo-slugfy", slugfy(u"Testamdo slugfy"))

    def test_used_accents(self):
        self.assertEquals(u"testando-se-e-slugfy",
                          slugfy(u"Testando sé é slugfy"))
