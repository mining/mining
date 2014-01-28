#!/usr/bin/env python
# -*- coding: utf-8 -*-
import riak

from wtforms.fields import TextField, TextAreaField, SelectField
from wtforms.validators import Required
from wtforms_tornado import Form


class ConnectionForm(Form):
    name = TextField(validators=[Required()])
    conection = TextField(validators=[Required()])


class CubeForm(Form):
    myClient = riak.RiakClient(protocol='http',
                               http_port=8098,
                               host='127.0.0.1')
    myBucket = myClient.bucket('openmining-admin')

    bconnection = myBucket.get('connection').data

    try:
        CONNECTION = tuple([(c['slug'], c['name']) for c in bconnection])
    except:
        CONNECTION = tuple()

    name = TextField(validators=[Required()])
    conection = SelectField(choices=CONNECTION, validators=[Required()])
    sql = TextAreaField(validators=[Required()])
