#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import os
import ast
import unicodedata
import ConfigParser
from bson import ObjectId
from datetime import datetime
from bottle import request

from mining.settings import PROJECT_PATH


def slugfy(text):
    try:
        slug = unicodedata.normalize("NFKD", text).encode("UTF-8", "ignore")
    except:
        slug = text
    slug = re.sub(r"[^\w]+", " ", slug)
    slug = "-".join(slug.lower().strip().split())
    if not slug:
        return None
    return slug


def conf(section, ini="mining.ini"):
    config = ConfigParser.ConfigParser()
    if os.path.isfile(os.path.join(PROJECT_PATH, ini)):
        config.read(os.path.join(PROJECT_PATH, ini))
    else:
        config.read(os.path.join(PROJECT_PATH, "mining.sample.ini"))
    _dict = {}
    options = config.options(section)

    for option in options:
        try:
            _dict[option] = ast.literal_eval(config.get(section, option))
        except:
            try:
                _dict[option] = config.get(section, option)
            except:
                _dict[option] = None

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
    except TypeError:
        return object


def query_field(f):
    ret = {}
    value = request.GET.get(f)
    if value:
        s = f.split('__')
        ret['action'] = s[0]
        ret['field'] = s[1]
        ret['operator'] = s[2]
        ret['value'] = value
    return ret
