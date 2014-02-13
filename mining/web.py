#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from tornado.web import RequestHandler


class SSEHandler(RequestHandler):
    def initialize(self):
        self.set_header("Content-Type", "text/event-stream")
        self.set_header("Cache-Control", "no-cache")

    def emit(self, data, event=None):
        response = u''
        encoded_data = json.dumps(data)

        if event is not None:
            response += u'event: ' + unicode(event).strip() + u'\n'

        response += u'data: ' + encoded_data.strip() + u'\n\n'

        self.write(response)
        self.flush()
