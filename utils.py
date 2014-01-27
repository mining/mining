#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pandas import tslib


def fix_render(value):
    if type(value) is str:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(value.decode('latin1'))
    elif type(value) is tslib.Timestamp:
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def pandas_to_dict(df):
    return [{colname: fix_render(row[i])
             for i, colname in enumerate(df.columns)}
            for row in df.values]
