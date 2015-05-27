#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import sys
import click

from bottle import static_file, Bottle, run, view
from bottle import TEMPLATE_PATH as T
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.auth.decorator import login

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from beaker.middleware import SessionMiddleware

from mining.controllers.api import api_app
from mining.controllers.data import data_app
from mining.utils import conf
from mining.auth import auth
from mining.settings import TEMPLATE_PATH, STATIC_PATH
from mining.celeryc import celery_app
from mining.bin.scheduler import scheduler_app
from mining.bin.demo.build_admin import build


reload(sys)
sys.setdefaultencoding('utf-8')


T.insert(0, TEMPLATE_PATH)

session_opts = {
    'session.type': 'file',
    'session.data_dir': '/tmp/openmining.data',
    'session.lock_dir': '/tmp/openmining.lock',
    'session.cookie_expires': 50000,
    'session.auto': True
}

app = SessionMiddleware(Bottle(), session_opts)
app.wrap_app.mount('/api', api_app)
app.wrap_app.mount('/data', data_app)

app.wrap_app.install(auth)


@app.wrap_app.route('/assets/<path:path>', name='assets')
def static(path):
    yield static_file(path, root=STATIC_PATH)


@app.wrap_app.route('/')
@login()
@view('index.html')
def index():
    return {'get_url': app.wrap_app.get_url,
            'protocol': conf('openmining')['protocol'],
            'lang': conf('openmining')['lang']}


@app.wrap_app.route('/login')
@view('login.html')
def login():
    return {'get_url': app.wrap_app.get_url,
            'lang': conf('openmining')['lang']}


@click.group()
def cmds():
    pass


@cmds.command()
@click.option('--port', type=int, help=u'Set application server port!')
@click.option('--ip', type=str, help=u'Set application server ip!')
@click.option('--debug', default=False,
              help=u'Set application server debug!')
def runserver(port, ip, debug):

    if debug is None:
        server = WSGIServer((ip, port), app, handler_class=WebSocketHandler)
        server.serve_forever()

    click.echo(u'OpenMining start server at: {}:{}'.format(ip, port))
    run(app=app, host=ip, port=port, debug=debug,
        reloader=True, server=GeventWebSocketServer)


@cmds.command()
@click.option('--concurrency', type=int, default=4,
              help="""Number of child processes processing the queue. The
              default is the number of CPUs available on your system.""")
def celery(concurrency):
    click.echo(u'OpenMining start tasks')
    args = ["celery", "worker", "--concurrency={}".format(concurrency)]
    celery_app.start(args)


@cmds.command()
def scheduler():
    click.echo(u'OpenMining start scheduler')
    scheduler_app()


@cmds.command()
@click.option('--level', type=int, default=0,
              help="What level of data volume?")
def build_demo(level):
    click.echo(u'OpenMining load demo system')
    build(level)


if __name__ == "__main__":
    default_map = {"runserver": conf('openmining')}
    default_map["runserver"]["debug"] = False
    cmds(default_map=default_map)
