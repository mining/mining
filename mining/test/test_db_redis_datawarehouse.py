#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json

from redis import StrictRedis

from mining.db import DataWarehouse


class connecion_via_drive_test(unittest.TestCase):
    def test_connection(self):
        DW = DataWarehouse()
        self.assertTrue(isinstance(DW.conn(), StrictRedis))


class save_via_drive_test(unittest.TestCase):
    def test_save_application_json(self):
        DW = DataWarehouse()
        DW.save('test_1', {"id": 1, "name": "Open Mining"})
        r = StrictRedis()
        self.assertEquals(r.get('test_1'), '{"id": 1, "name": "Open Mining"}')

    def test_save_text(self):
        DW = DataWarehouse()
        DW.save('test_2', "Open Mining", content_type='application/text')
        r = StrictRedis()
        self.assertEquals(r.get('test_2'), "Open Mining")


class get_via_drive_test(unittest.TestCase):
    def test_get_application_json(self):
        r = StrictRedis()
        data = {"id": 1, "name": "Open Mining"}
        r.set('test_get_1', json.dumps(data))
        DW = DataWarehouse()
        self.assertEquals(DW.get("test_get_1"), data)

    def test_get_text(self):
        r = StrictRedis()
        r.set('test_get_2', "Open Mining")
        DW = DataWarehouse()
        self.assertEquals(
            DW.get("test_get_2", content_type='application/text'),
            "Open Mining")
