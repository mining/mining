#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
from bottle import Bottle, abort
from bottle.ext.websocket import websocket

from geventwebsocket import WebSocketError


stream_app = Bottle()


@stream_app.route('/data', apply=[websocket])
def data(ws):
    if not ws:
        abort(400, 'Expected WebSocket request.')

    i = 1
    while True:
        try:
            ws.send("Your message was: ")
            if i == 10:
                break
            time.sleep(0.1)
        except WebSocketError:
            break
        i += 1
