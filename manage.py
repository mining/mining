#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import tornado.ioloop
import tornado.web
import tornado.autoreload

from tornado.options import parse_command_line, define, options


define('port', default=8888)
define('template_path', default='templates')
define('PROJECT_PATH', default=os.path.join(
    os.path.abspath(os.path.dirname(__file__))))

settings = dict(
    debug=True,
    gzip=True,
    autoreload=True,
    template_path="{}/{}".format(options.PROJECT_PATH, options.template_path))


def main():
    from urls import URLS

    application = tornado.web.Application(URLS, **settings)

    print "openmining.io server starting..."

    def fn():
        print "openmining.io before reloading..."

    parse_command_line()
    application.listen(options.port)
    tornado.autoreload.add_reload_hook(fn)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
