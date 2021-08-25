# -*- coding: utf-8 -*-

# 参数文件
import json


class Properties(object):

    def load(self):
        return json.load(open('config.json'))


config = Properties().load()
