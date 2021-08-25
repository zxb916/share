# -*- coding: utf-8 -*-
import datetime
from time import sleep
import tushare as ts
from common.config.config import config
from threadpool.buythread import BuyThread
import requests
import threading
from common.util.redis_util import redis


class BuyStock(object):
    """ 所有买入股票的策略都实现此方法 """

    def buy(self, code):
        raise NotImplementedError()


class LowPrice(BuyStock):
    def buy(self, code):
        time_window = config['trade']['buy_time_window'] * 60 / config['trade']['frequency']
        back_result, _Threads = [], []
        t = BuyThread(target=BuyThread.threadItem, args=(BuyThread, int(time_window), code,))
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
                print("买入股票 %s 价格 %s 次数 %s 时间 %s" % (result[0], result[1], result[2], result[3]))
                # if not config['trade']['simulate']:
                # os.system("D:\\DevelopeSoft\\pycharm\\workspace\\shares\\mp3\\alert.mp3")
                # os.system(os.getcwd() + "\\mp3\\alert.mp3")
                if config['trade']['redis_save']:
                    redis.buy_save(result)
                myurl = "http://127.0.0.1:9090/trade/buy"
                datas = {"code": result[0], "price": result[1]}
                try:
                    requests.post(myurl, data=datas)
                except Exception:
                    print("发送成功")
                    raise
        print("当前运行的线程数%d" % threading.activeCount())
        print('完成')


class PmHalfTwo(BuyStock):
    def buy(self, code):
        if not config['trade']['simulate']:
            print("------------------判断当前时间是否是交易时间-----------------")
            while True:
                # 范围时间
                d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:30:00', '%Y-%m-%d%H:%M:%S')
                d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:32:00',
                                                     '%Y-%m-%d%H:%M:%S')
                # 当前时间
                n_time = datetime.datetime.now()
                # 判断当前时间是否在范围时间内
                if d_time < n_time < d_time1:
                    print("------------------交易时间内-----------------")
                    break
                else:
                    print("------------------不在交易时间内-----------------")
                    sleep(30)
            myurl = "http://127.0.0.1:9090/trade/buy"
            data = ts.get_realtime_quotes(symbols=code)
            datas = {"code": code, "price": float(data['price'])}
            try:
                requests.post(myurl, data=datas)
            except Exception:
                print("发送成功")
                raise


class AmHalfNine(BuyStock):
    def buy(self, code):
        if not config['trade']['simulate']:
            print("------------------判断当前时间是否是交易时间-----------------")
            while True:
                # 范围时间
                d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '14:30:00',
                                                    '%Y-%m-%d%H:%M:%S')
                d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '14:32:00',
                                                     '%Y-%m-%d%H:%M:%S')
                # 当前时间
                n_time = datetime.datetime.now()
                # 判断当前时间是否在范围时间内
                if d_time < n_time < d_time1:
                    print("------------------交易时间内-----------------")
                    break
                else:
                    print("------------------不在交易时间内-----------------")
                    sleep(30)
            myurl = "http://127.0.0.1:9090/trade/buy"
            data = ts.get_realtime_quotes(symbols=code)
            datas = {"code": code, "price": float(data['price'])}
            try:
                requests.post(myurl, data=datas)
            except Exception:
                print("发送成功")
                raise


class BuyTest(BuyStock):
    def buy(self, code):
        myurl = "http://127.0.0.1:9090/trade/buy"
        data = ts.get_realtime_quotes(symbols=code)
        datas = {"code": code, "price": float(data['price'])}
        try:
            requests.post(myurl, data=datas)
        except Exception:
            print("发送成功")
            raise
