#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import schedule

from bottle.ext.mongo import MongoPlugin

from settings import ADMIN_BUCKET_NAME, MONGO_URI
from bin.mining import run


def job(slug):
    run(slug)

"""
schedule.every(1).minutes.do(cube)
schedule.every().hour.do(cube)
schedule.every().day.at("16:04").do(cube)
"""

mongo = MongoPlugin(uri=MONGO_URI, db=ADMIN_BUCKET_NAME,
                    json_mongo=True).get_mongo()

for s in mongo['scheduler'].find():
    t = getattr(schedule.every(s.get('interval')), s.get('type'))
    t.do(job, slug=s.get('slug'))

while True:
    schedule.run_pending()
    time.sleep(1)
