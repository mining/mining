# -*- coding: utf-8 -*-
import traceback
import requests

from mining.celeryc import celery_app
from mining.utils import conf, log_it
from mining.utils._pandas import CubeJoin
from mining.models.cube import Cube

from bottle.ext.mongo import MongoPlugin


@celery_app.task
def process(_cube):
    try:
        log_it("START: {}".format(_cube['slug']), "bin-mining")

        mongo = MongoPlugin(
            uri=conf("mongodb")["uri"],
            db=conf("mongodb")["db"],
            json_mongo=True).get_mongo()

        c = Cube(_cube)
        if _cube.get('type') == 'relational':
            c.load()
            c.frame()
            c.save()
        elif _cube.get('type') == 'cube_join':
            c.environment(_cube.get('type'))
            cube_join = CubeJoin(_cube)
            c._data(cube_join.none())
            c._keys(cube_join.none().columns.values)
            c.frame()
            c.save()
        elif _cube.get('type') == 'url':
            c._data(requests.get(_cube.get('connection')).text)
            c.frame(data_type=_cube.get('url_type'))
            c.save()

    except Exception, e:
        log_it(e, "bin-mining")
        log_it(traceback.format_exc(), "bin-mining")
        _cube['run'] = False
        mongo['cube'].update({'slug': _cube['slug']}, _cube)

    log_it("END: {}".format(_cube['slug']), "bin-mining")
