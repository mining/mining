#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wtforms.fields import TextField, TextAreaField
from wtforms.fields import SelectField, SelectMultipleField
from wtforms.validators import Required
from wtforms_tornado import Form

from .models import MyAdminBucket


def ObjGenerate(bucket, key, value=None, _type=tuple):
    bconnection = MyAdminBucket.get(bucket).data

    try:
        if _type is tuple:
            return _type(
                [('', '')] + [(c[key], c[value]) for c in bconnection])
        return _type(c[key] for c in bconnection)
    except:
        return _type()


class ConnectionForm(Form):
    name = TextField(validators=[Required()])
    conection = TextField(validators=[Required()],
                          description=u"mysql://user:pass@127.0.0.1/db")


class CubeForm(Form):
    name = TextField(validators=[Required()])
    conection = SelectField(validators=[Required()],
                            choices=ObjGenerate('connection', 'slug', 'name'))
    sql = TextAreaField(validators=[Required()])


class ElementForm(Form):
    ELEMENT_TYPE = ((u'', u''),
                    (u'grid', u'Grid'),
                    (u'chart_line', u'Chart line'),
                    (u"chart_bar", u"Chart bar"))

    name = TextField(validators=[Required()])
    type = SelectField(choices=ELEMENT_TYPE, validators=[Required()])
    cube = SelectField(choices=ObjGenerate('cube', 'slug', 'name'),
                       validators=[Required()])


class DashboardForm(Form):
    name = TextField(validators=[Required()])
    element = SelectMultipleField(
        validators=[Required()],
        choices=ObjGenerate('element', 'slug', 'name'))
