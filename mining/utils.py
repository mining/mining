#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodedata
import re
from decimal import Decimal

from pandas import tslib, date_range


def fix_render(value):
    if type(value) is str:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(value.decode('latin1'))
    elif type(value) is tslib.Timestamp:
        return value.strftime("%Y-%m-%d %H:%M:%S")
    elif type(value) is Decimal:
        return str(value)
    return value


def pandas_to_dict(df):
    return [{colname: fix_render(row[i])
             for i, colname in enumerate(df.columns)}
            for row in df.values]


def slugfy(text):
    slug = unicodedata.normalize("NFKD", text).encode("UTF-8", "ignore")
    slug = re.sub(r"[^\w]+", " ", slug)
    slug = "-".join(slug.lower().strip().split())
    if not slug:
        return None
    return slug


def df_generate(df, argument, str_field):
    s = str_field.split('__')
    field = s[1]
    operator = s[2]
    value = argument(str_field)

    try:
        t = s[3]
    except:
        t = "str"

    if t == "date":
        try:
            mark = s[4].replace(":", "%")
        except:
            mark = "%Y-%m-%d"

    if operator == "gte":
        return (df[field] > value)
    elif operator == "lte":
        return (df[field] < value)
    elif operator == "is":
        return (df[field] == value)
    elif operator == "in":
        return u"{} in {}".format(field, [i for i in value.split(',')])
    elif operator == "notin":
        return u"{} not in {}".format([i for i in value.split(',')], field)
    elif operator == "between":
        _range = []
        between = value.split(":")

        if t == "date":
            _range = [i.strftime(mark)
                      for i in date_range(between[0], between[1]).tolist()]
        elif t == "int":
            _range = [i for i in xrange(between[0], between[1]+1)]

        return u"{} in {}".format(field, _range)
