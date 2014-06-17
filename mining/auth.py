#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle.ext import auth

from mining.utils import conf, __from__


auth_engine = __from__(conf('auth')['engine'])
if auth_engine == object:
    print 'Set valid auth engine'
    exit(0)

auth_import = conf('auth')['engine'].split('.')[-1]

callback = u"{}://{}".format(
    conf('openmining')['protocol'],
    conf('openmining')['domain'])
if conf('openmining')['domain_port'] not in ['80', '443']:
    callback = "{}:{}".format(callback, conf('openmining')['domain_port'])

if auth_import == 'Google':
    engine = auth_engine(
        conf('auth')['key'], conf('auth')['secret'], callback)
elif auth_import == 'Facebook':
    #  Not working requered parans
    engine = auth_engine()
elif auth_import == 'Twitter':
    #  Not working requered parans
    engine = auth_engine()
else:
    engine = auth_engine(callback_url=callback, field="username")

auth = auth.AuthPlugin(engine)
