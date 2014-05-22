#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle.ext import auth

from utils import conf


try:
    auth_import = conf('auth')['engine'].split('.')[-1]
    auth_from = u".".join(conf('auth')['engine'].split('.')[:-1])
    auth_engine = getattr(__import__(auth_from, fromlist=[auth_import]),
                          auth_import)
except:
    print 'Set valid auth engine'
    exit(0)

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
