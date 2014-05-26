#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import os
import unicodedata
import ConfigParser
from decimal import Decimal
from datetime import date, datetime
from bson import ObjectId

from pandas import tslib, date_range, bdate_range, concat, DataFrame
from settings import PROJECT_PATH


def fix_type(value):
    if type(value) is str:
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            return value.decode('latin1')
    elif type(value) is tslib.Timestamp:
        try:
            return value.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime(1900, 01, 01, 00, 00, 00).strftime()
    elif type(value) is date or type(value) is datetime:
        try:
            return value.strftime("%Y-%m-%d")
        except ValueError:
            return datetime(1900, 01, 01).strftime()
    elif type(value) is Decimal:
        return float(value)
    return value


def fix_render(_l):
    return dict(map(lambda (k, v): (k, fix_type(v)), _l.iteritems()))


def slugfy(text):
    slug = unicodedata.normalize("NFKD", text).encode("UTF-8", "ignore")
    slug = re.sub(r"[^\w]+", " ", slug)
    slug = "-".join(slug.lower().strip().split())
    if not slug:
        return None
    return slug


def df_generate(df, value, str_field):
    s = str_field.split('__')
    field = s[1]
    try:
        operator = s[2]
    except:
        operator = "is"

    try:
        t = s[3]
        if t == "int" and operator not in ["in", "notin", "between"]:
            value = int(value)
    except:
        t = "str"

    if t == "date":
        try:
            mark = s[4].replace(":", "%")
        except:
            mark = "%Y-%m-%d"
    elif t == "datetime":
        mark = "%Y-%m-%d %H:%M:%S"

    if operator == "gte":
        return u"{} >= {}".format(field, value)
    elif operator == "lte":
        return u"{} <= {}".format(field, value)
    elif operator == "is":
        if t == 'int':
            return u"{} == {}".format(field, value)
        return u"{} == '{}'".format(field, value)
    elif operator == "in":
        if t == 'int':
            return u"{} in {}".format(field,
                                      [int(i) for i in value.split(',')])
        return u"{} in {}".format(field, [i for i in value.split(',')])
    elif operator == "notin":
        if t == 'int':
            return u"{} not in {}".format([int(i) for i in value.split(',')],
                                          field)
        return u"{} not in {}".format([i for i in value.split(',')], field)
    elif operator == "between":
        _range = []
        between = value.split(":")

        if t == "date":
            _range = [i.strftime(mark)
                      for i in date_range(between[0], between[1]).tolist()]
        elif t == "datetime":
            _range = [i.strftime(mark)
                      for i in
                      date_range(between[0], between[1], freq="S").tolist()]
        elif t == "int":
            _range = [i for i in xrange(int(between[0]), int(between[1]) + 1)]

        return u"{} in {}".format(field, _range)


def conf(section):
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(PROJECT_PATH, 'mining.ini'))
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


def DataFrameSearchColumn(df, colName, value, operator='like'):
    ndf = DataFrame()
    for idx, record in df[colName].iteritems():
        check = True
        if operator == 'like' and value in str(record):
            check = True

        if operator == 'regex' and re.search(value, str(record)):
            check = True

        if check:
            ndf = concat([df[df[colName] == record], ndf], ignore_index=True)

    return ndf
