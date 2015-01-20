#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from decimal import Decimal
from datetime import date, datetime

from pandas import DataFrame, date_range, tslib, concat

from mining.utils import conf
from mining.db import DataWarehouse


def fix_type(value):
    if type(value) is str:
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            return value.decode('latin1')
    elif type(value) in [int, float]:
        return value
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
    return unicode(value)


def fix_render(_l):
    return {k:fix_type(v) for k,v in _l.iteritems()}


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
                      date_range(between[0], between[1], freq="H").tolist()]
        elif t == "int":
            _range = [i for i in xrange(int(between[0]), int(between[1]) + 1)]

        return u"{} in {}".format(field, _range)


def DataFrameSearchColumn(df, field, value, operator):
    ndf = DataFrame()
    for idx, record in df[field].iteritems():
        if operator == 'regex' and re.search(value, str(record)):
            ndf = concat([df[df[field] == record], ndf], ignore_index=True)
    return ndf


class CubeJoin(object):
    def __init__(self, cube):
        self.cube = cube
        self.data = DataFrame({})
        method = getattr(self, cube.get('cube_join_type', 'none'))
        method()

    def inner(self):
        fields = [rel['field'] for rel in self.cube.get('relationship')]
        DW = DataWarehouse()
        for i, rel in enumerate(self.cube.get('relationship')):
            data = DW.get(rel['cube']).get('data')
            df = DataFrame(data)
            if i == 0:
                self.data = df
            else:
                self.data = self.data.merge(df, how='inner', on=fields[0])
        return self.data

    def left(self):
        fields = [rel['field'] for rel in self.cube.get('relationship')]
        self.data = DataFrame({fields[0]: []})
        DW = DataWarehouse()
        for rel in self.cube.get('relationship'):
            data = DW.get(rel['cube'])
            self.data = self.data.merge(DataFrame(data.get('data')),
                how='outer', on=fields[0])
        return self.data

    def append(self):
        self.data = DataFrame({})
        DW = DataWarehouse()
        self.data.append([DataFrame(
                          DW.get(rel['cube']).get('data'))
                          for rel in self.cube.get('relationship')],
                         ignore_index=True)
        return self.data

    def none(self):
        return self.data


def to_pdf(df, x=300, y=300):
    from reportlab.pdfgen.convas import Canvas

    c = Canvas('/tmp/out.pdf')
    c.drawAlignedString(x, y, str(df))
    c.showPage()
    c.save()
