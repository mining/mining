# -*- coding: utf-8 -*-
from .base import DataManager as BaseDataManager


class DataManager(BaseDataManager):
    def send(self, obj):
        self.data.append(obj)
