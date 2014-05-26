#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from webtest import TestApp

from controllers.api.user import user_app


class get_test(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(user_app)

    def test_route(self):
        self.assertEquals(u"200 OK", self.app.get("/").status)
