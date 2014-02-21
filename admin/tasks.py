#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import MyAdminBucket


def related_delete(bucket, slug, value):
    admin_items = {'connection': ['cube', 'element', 'dashboard'],
                   'cube': ['element', 'dashboard'],
                   'element': ['dashboard'],
                   'dashboard': []}

    for bucket in admin_items.get(bucket):
        get_bucket = MyAdminBucket.get(bucket).data or []
        get_bucket = [b for b in get_bucket if b.get(slug) != value]

        MyAdminBucket.new(bucket, data=get_bucket).store()

    return True
