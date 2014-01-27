#!/usr/bin/env python
# -*- coding: utf-8 -*-
def fix_str(value):
    try:
        return unicode(value)
    except UnicodeDecodeError:
        return unicode(value.decode('latin1'))


def pandas_to_dict(df):
    return [{colname: (fix_str(row[i]) if type(row[i]) is str else row[i])
             for i, colname in enumerate(df.columns)}
            for row in df.values]
