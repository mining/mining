#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import argparse

from bottle import static_file, Bottle, template, TEMPLATE_PATH, run

from gevent.pywsgi import WSGIServer

from controllers.api import api_app


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


@app.route('/asserts/<path:path>')
def static(path):
    yield static_file(path, root=u'{}/{}'.format(PROJECT_PATH, u'asserts'))


@app.route('/')
def index():
    return template('index.html')


def main():
    print u'OpenMining start server at: {}:{}'.format(args.ip,
                                                      args.port)

    if args.debug is None:
        from gevent import monkey

        monkey.patch_all()

        server = WSGIServer((args.ip, args.port), app)
        server.serve_forever()

    run(app=app, host=args.ip, port=args.port, debug=args.debug,
        reloader=True)


if __name__ == "__main__":
    main()
