#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import os
import unicodedata
import ConfigParser
from bson import ObjectId
from datetime import datetime

from mining.settings import PROJECT_PATH


def slugfy(text):
    slug = unicodedata.normalize("NFKD", text).encode("UTF-8", "ignore")
    slug = re.sub(r"[^\w]+", " ", slug)
    slug = "-".join(slug.lower().strip().split())
    if not slug:
        return None
    return slug


def conf(section, ini="mining.ini"):
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(PROJECT_PATH, ini))
    _dict = {}
    options = config.options(section)
    for option in options:
        try:
            _dict[option] = config.get(section, option)
        except:
            _dict[option] = None

    if 'sql_conn_params' in options:
        import ast

        _dict['sql_conn_params'] = ast.literal_eval(_dict['sql_conn_params'])
    else:
        _dict['sql_conn_params'] = {}

    return _dict


def log_it(s, name=u"core"):
    with open("/tmp/openmining-{}.log".format(name), "a") as log:
        msg = u"{} => {}\n".format(datetime.now(), s)
        log.write(msg.encode('utf-8'))


def parse_dumps(obj):
    if isinstance(obj, datetime):
        return str(obj.strftime("%Y-%m-%d %H:%M:%S"))
    if isinstance(obj, ObjectId):
        return str(obj)
    return json.JSONEncoder.default(obj)


def __from__(path):
    try:
        _import = path.split('.')[-1]
        _from = u".".join(path.split('.')[:-1])
        return getattr(__import__(_from, fromlist=[_import]), _import)
    except:
        return object
