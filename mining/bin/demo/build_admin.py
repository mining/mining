#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import os
from mining.tasks import process
import sqlite3


def build(level=0):
    demo_path = os.path.abspath(os.path.dirname(__file__))
    try:
        os.remove(os.path.join(demo_path, 'demo.db'))
    except OSError:
        pass
    conn = sqlite3.connect('{}'.format(os.path.join(demo_path, 'demo.db')))
    cur = conn.cursor()
    f = open('{}'.format(os.path.join(demo_path, 'base.sql')), 'r')
    sql_str = f.read()
    print 'INSERT SQLITE DATA'
    cur.executescript(sql_str)
    conn.commit()
    f.close()
    if level > 0:
        l = open(os.path.join(demo_path, 'people.sql'), 'r').read()
        print 'INSERT SQLITE DATA LEVEL {}'.format(level)
        for i in xrange(level):
            cur.executescript(l)
            conn.commit()
            print "LEVEL {} COMMIT".format(i)
    cur.close()

    url_api = {
        'user': "http://127.0.0.1:8888/api/user",
        'connection': "http://127.0.0.1:8888/api/connection",
        'cube': "http://127.0.0.1:8888/api/cube",
        'element': "http://127.0.0.1:8888/api/element",
        'dashboard': "http://127.0.0.1:8888/api/dashboard"
    }
    data = {
        'user': {'username': 'admin', 'password': 'admin', 'rule': 'root'},
        'connection': {
            "connection": 'sqlite:///{}'.format(
                os.path.join(demo_path, 'demo.db')),
            "name": "DEMO"
        },
        'cube': [
            {
                "status": False,
                "run": False,
                "name": "Sales",
                "slug": "sales",
                "connection": "demo",
                "sql": "select * from SALE;",
                "scheduler_status": False,
                "type": "relational"
            },
            {
                "status": False,
                "run": False,
                "name": "People",
                "slug": "people",
                "connection": "demo",
                "sql": "select * from people;",
                "scheduler_status": False,
                "type": "relational"
            },
            {
                "status": False,
                "run": False,
                "name": "Product Sales",
                "slug": "product-sales",
                "connection": "demo",
                "sql": "select * from SALE_PRODUCT;",
                "scheduler_status": False,
                "type": "relational"
            },
            {
                "status": False,
                "run": False,
                "name": "Sales by month",
                "slug": "sales-by-month",
                "connection": "demo",
                "sql": "SELECT  strftime('%Y-%m', sale_at) as month, SUM(value) \
                        as total\nFROM    sale\n\
                        GROUP BY strftime('%Y-%m', sale_at)",
                "scheduler_status": False,
                "type": "relational",
                "slug": "sales-by-month"
            }
        ],
        'element': [
            {
                "alias": {

                },
                "cube": "people",
                "field_serie": None,
                "field_x": None,
                "field_y": None,
                "name": "People Grid",
                "orderby": [
                    "full_name"
                ],
                "orderby__order": [
                    "1"
                ],
                "scheduler_status": False,
                "show_fields": [
                    "id_people",
                    "full_name",
                    "gender",
                    "age",
                    "country",
                    "created_at"
                ],
                "type": "grid",
                "widgets": [
                    {
                        "field": "country",
                        "type": "distinct",
                        "label": "Country"
                    }
                ]
            },
            {
                "alias": {

                },
                "cube": "sales-by-month",
                "field_serie": None,
                "field_x": "month",
                "field_y": "total",
                "name": "Sales Bar",
                "scheduler_status": False,
                "show_fields": [
                    "month",
                    "total"
                ],
                "type": "chart_bar"
            },
            {
                "orderby": [
                    "sale_at"
                ],
                "cube": "sales",
                "name": "Sales Grid",
                "show_fields": [
                    "id_sale",
                    "id_people",
                    "value",
                    "paid",
                    "sale_at"
                ],
                "widgets": [],
                "alias": {

                },
                "field_x": None,
                "field_y": None,
                "scheduler_status": False,
                "orderby__order": [
                    "0"
                ],
                "type": "grid",
                "field_serie": None
            }
        ],
        'dashboard': {
            "scheduler_status": False,
            "element": [
                {
                    "id": "people-grid",
                    "label": "People Grid"
                },
                {
                    "id": "sales-bar",
                    "label": "Sales Bar"
                },
                {
                    "id": "sales-grid",
                    "label": "Sales Grid"
                }
            ],
            "slug": "demo",
            "name": "Demo"
        }
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    print 'CREATE USER admin'
    requests.post(url_api.get('user'), data=json.dumps(data.get('user')),
                  headers=headers)
    print 'CREATE connection'
    requests.post(url_api.get('connection'),
                  data=json.dumps(data.get('connection')),
                  headers=headers)
    print 'CREATE cube'
    for cb in data.get('cube'):
        requests.post(url_api.get('cube'), data=json.dumps(cb),
                      headers=headers)
        print 'RUNNING cube {}'.format(cb.get('slug'))
        process(cb)

    print 'CREATE element'
    for el in data.get('element'):
        print '--> {}'.format(el.get('name'))
        requests.post(url_api.get('element'), data=json.dumps(el),
                      headers=headers)

    print 'CREATE dashboard'
    requests.post(url_api.get('dashboard'),
                  data=json.dumps(data.get('dashboard')),
                  headers=headers)
