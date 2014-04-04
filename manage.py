#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import sys
import argparse

from bottle import static_file, Bottle, run, view
from bottle import TEMPLATE_PATH as T
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.auth.decorator import login

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from beaker.middleware import SessionMiddleware

from controllers.api import api_app
from controllers.stream import stream_app
from controllers.export import export_app

from utils import conf
from auth import auth
from settings import TEMPLATE_PATH, STATIC_PATH


reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description=u'OpenMining Application Server')
parser.add_argument('--port', help=u'Set application server port!',
                    type=int, default=conf('openmining')['port'])
parser.add_argument('--ip', help=u'Set application server IP!',
                    type=str, default=conf('openmining')['ip'])
parser.add_argument('--debug', '-v', help=u'Set application server debug!',
                    action='count')
args = parser.parse_args()


T.insert(0, TEMPLATE_PATH)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

app = SessionMiddleware(Bottle(), session_opts)
app.wrap_app.mount('/api', api_app)
app.wrap_app.mount('/stream', stream_app)
app.wrap_app.mount('/export', export_app)

app.wrap_app.install(auth)


@app.wrap_app.route('/assets/<path:path>', name='assets')
def static(path):
    yield static_file(path, root=STATIC_PATH)


@app.wrap_app.route('/')
@login(auth)
@view('index.html')
def index():
    return {'get_url': app.wrap_app.get_url}


@app.wrap_app.route('/login')
@view('login.html')
def login():
    return {'get_url': app.wrap_app.get_url}


def main():
    print u'OpenMining start server at: {}:{}'.format(args.ip,
                                                      args.port)

    if args.debug is None:
        server = WSGIServer((args.ip, args.port), app,
                            handler_class=WebSocketHandler)
        server.serve_forever()

    run(app=app, host=args.ip, port=args.port, debug=args.debug,
        reloader=True, server=GeventWebSocketServer)


if __name__ == "__main__":
    main()
