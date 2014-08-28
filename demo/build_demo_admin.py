#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import os
from mining.bin.cube import run
import sqlite3

conn = sqlite3.connect('demo.db')
f = open('demo_base.sql', 'r')
sql_str = f.read()
conn.executescript(sql_str)
db_path = os.path.abspath('demo.db')

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
        "connection": db_path,
        "name": "DEMO"
    },
    'cubes': [
        {
            "status": False,
            "run": False,
            "name": "Sales",
            "connection": "demo",
            "sql": "select * from SALE;",
            "scheduler_status": False,
            "type": "relational"
        },
        {
            "status": False,
            "run": False,
            "name": "People",
            "connection": "demo",
            "sql": "select * from people;",
            "scheduler_status": False,
            "type": "relational"
        },
        {
            "status": False,
            "run": False,
            "name": "Product Sales",
            "connection": "demo",
            "sql": "select * from SALE_PRODUCT;",
            "scheduler_status": False,
            "type": "relational"
        },
        {
            "status": False,
            "run": False,
            "name": "Sales by month",
            "connection": "demo",
            "sql": "SELECT  strftime('%%Y-%%m', sale_at) as month, SUM(value) as total\nFROM    sale\nGROUP BY strftime('%%Y-%%m', sale_at)",
            "scheduler_status": False,
            "type": "relational",
            "slug": "sales-by-month"
        }
    ],
    'elements': [
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
            "slug": "people-grid",
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
            "slug": "sales-bar",
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
            "slug": "sales-grid",
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
r = requests.post(url_api.get('user'), data=json.dumps(data.get('user')),
                  headers=headers)
r = requests.post(url_api.get('connection'),
                  data=json.dumps(data.get('connection')),
                  headers=headers)
for cb in data.get('cube'):
    r = requests.post(url_api.get('cube'), data=json.dumps(cb),
                      headers=headers)
    run(cb.get('slug'))

for el in data.get('element'):
    r = requests.post(url_api.get('element'), data=json.dumps(el),
                      headers=headers)
r = requests.post(url_api.get('dashboard'),
                  data=json.dumps(data.get('dashboard')),
                  headers=headers)