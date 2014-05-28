#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json


url = "http://127.0.0.1:8888/api/user"
data = {'username': 'admin', 'password': 'admin', 'rule': 'root'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)
