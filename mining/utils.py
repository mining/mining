#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodedata
import re
from decimal import Decimal

from pandas import tslib


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
