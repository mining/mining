#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import argparse

from bottle import static_file, Bottle, template, TEMPLATE_PATH, run

from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from bottle.ext.websocket import GeventWebSocketServer

from controllers.api import api_app
from controllers.stream import stream_app


reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description=u'OpenMining Application Server')
parser.add_argument('--port', help=u'Set application server port!',
                    type=int, default=8888)
parser.add_argument('--ip', help=u'Set application server IP!',
                    type=str, default=u'0.0.0.0')
parser.add_argument('--debug', '-v', help=u'Set application server debug!',
                    action='count')
args = parser.parse_args()

PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))
TEMPLATE_PATH.insert(0, u'{}/{}'.format(PROJECT_PATH, 'views'))

app = Bottle()
app.mount('/api', api_app)
app.mount('/stream', stream_app)


@app.route('/asserts/<path:path>')
def static(path):
    yield static_file(path, root=u'{}/{}'.format(PROJECT_PATH, u'asserts'))


@app.route('/')
def index():
    return template('index.html')


def main():
    print u'OpenMining start server at: {}:{}'.format(args.ip,
                                                      args.port)

    monkey.patch_all()
    if args.debug is None:
        server = WSGIServer((args.ip, args.port), app,
                            handler_class=WebSocketHandler)
        server.serve_forever()

    run(app=app, host=args.ip, port=args.port, debug=args.debug,
        reloader=True, server=GeventWebSocketServer)


if __name__ == "__main__":
    main()
