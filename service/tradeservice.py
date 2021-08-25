# -*- coding: utf-8 -*-
import threading

import requests
import tushare as ts

from common.config.config import config
from context.context import BuyContext
from threadpool.selathread import SelaThread


def buy(instance, code):
    buy_context = BuyContext(instance)
    buy_context.buy(code)


def get_data(codes):
    result = []
    for code in codes:
        data = ts.get_realtime_quotes(symbols=code)
        currentprice = float(data['price'])
        pre_close = float(data['pre_close'])
        increase = (currentprice - pre_close) / pre_close
        temp = code + "当前股价:" + str(currentprice) + ",涨幅:" + str(round(increase, 3))
        result.append(temp)
    return result


def sela(code):
    time_window = config['trade']['sela_time_window'] * 60 / config['trade']['frequency']
    back_result, _Threads = [], []
    t = SelaThread(target=SelaThread.threadItem, args=(SelaThread, int(time_window), code,))
    # 设置为守护线程，不会因主线程结束而中断
    t.setDaemon(True)
    t.setName(code)
    t.start()
    _Threads.append(t)
    for t in _Threads:
        # 子线程全部加入，主线程等所有子线程运行完毕
        t.join()
        back_result.append(t.get_result())
    print('主线程等待')
    print("------------------等待结果-----------------")
    for t in _Threads:
        if t.get_result() is not None:
            print(t.get_result())
            result = str.split(t.get_result(), '-')
            print("卖出股票 %s 价格 %s 次数 %s 时间 %s" % (result[0], result[1], result[2], result[3]))
            # if not config['trade']['simulate']:
            # os.system("D:\\DevelopeSoft\\pycharm\\workspace\\shares\\mp3\\alert.mp3")
            # os.system(os.getcwd() + "\\mp3\\alert.mp3")
            myurl = "http://127.0.0.1:9090/trade/sela"
            datas = {"code": result[0], "price": result[1]}
            try:
                requests.post(myurl, data=datas)
            except Exception:
                print("发送成功")
                raise
    print("当前运行的线程数%d" % threading.activeCount())
    print('完成')
