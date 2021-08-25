# coding:utf-8


import threading
from queue import Queue

import tushare as ts

from common.config.config import config
from threadpool.buyAnalythread import BuyAnalyze
from threadpool.realtime import RealTime


class BuyThread(threading.Thread):
    """重写多线程，使其能够返回值"""

    def __init__(self, target=None, args=(), ):
        print(str(config['trade']['buy_time_window']) + "分钟窗口启动")
        super(BuyThread, self).__init__()
        self.func = target
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

    def threadItem(self, count, code):
        queue1 = Queue()
        queue2 = Queue()
        datas = ts.get_tick_data(code=code, date=config['trade']['simulate-day'], src=config['data_source'])
        if not config['trade']['simulate']:
            analy = BuyAnalyze(count, queue1, queue2)
        else:
            # 设置模拟频率
            count = round((len(datas) - 3) * config['trade']['buy_time_window'] * 60 / 14400)
            analy = BuyAnalyze(count, queue1, queue2)
        # 启动分析线程
        analy.start()
        realtime = RealTime(queue1, queue2, True)
        price = realtime.get_realtime(code)
        return price
