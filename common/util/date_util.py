# -*- coding: UTF-8 -*-
import time
import datetime


class DateUtil:

    @staticmethod
    def get_today():
        today = datetime.datetime.now().weekday()
        if today == 5:
            day = datetime.datetime.now() + datetime.timedelta(days=-1)
            day = day.strftime('%Y-%m-%d')
        elif today == 6:
            day = datetime.datetime.now() + datetime.timedelta(days=-2)
            day = day.strftime('%Y-%m-%d')
        else:
            day = time.strftime("%Y-%m-%d", time.localtime())
        return day

    @staticmethod
    def get_yesterday():
        today = datetime.datetime.now().weekday()
        now_time = datetime.datetime.now()
        if today == 5:
            day = now_time + datetime.timedelta(days=-2)
        elif today == 6:
            day = now_time + datetime.timedelta(days=-3)
        else:
            day = now_time + datetime.timedelta(days=-1)
        return day.strftime('%Y-%m-%d')
