# coding:utf-8
import datetime
import threading

import tushare as ts
from time import sleep

from common.config.config import config


class RealTime:

    def __init__(self, queue1, queue2, flag):
        self.flag = flag
        self.queue1 = queue1
        self.queue2 = queue2
        print('开始获取实时数据')

    # 获取实时数据
    def get_realtime(self, code):
        sleep_time = config['trade']['frequency']
        if not config['trade']['simulate']:
            print("------------------判断当前时间是否是交易时间-----------------")
            while True:
                # 范围时间
                d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:25:00', '%Y-%m-%d%H:%M:%S')
                d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '15:00:00',
                                                     '%Y-%m-%d%H:%M:%S')
                d_time2 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:30:00',
                                                     '%Y-%m-%d%H:%M:%S')
                # 当前时间
                n_time = datetime.datetime.now()
                # 判断当前时间是否在范围时间内
                if d_time < n_time < d_time1:
                    print("start")
                    break
                print("------------------当前不在交易时间内-----------------")
                sleep(30)
            print("------------------实时获取当前股价-----------------")
            while True:
                sleep(sleep_time)
                data = ts.get_realtime_quotes(symbols=code)
                currentprice = float(data['price'])
                close_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + str(data['time'][0]),
                                                        '%Y-%m-%d%H:%M:%S')
                if currentprice - low < 0:
                    low = currentprice
                    print("%s ------股价将会下降 ,当前股价 %.2f ------" % (threading.currentThread().getName(), currentprice))
                elif currentprice - high > 0:
                    high = currentprice
                    print(" %s ------股价将会上升 ,当前股价 %.2f ------" % (threading.currentThread().getName(), currentprice))
                count = count + 1
                if self.flag:
                    print("找到了----")
                    break
                else:
                    # 拐点
                    # 时间窗口统计
                    self.queue1.put(currentprice)
                    msg = self.queue2.get()
                    if selapot == 0:
                        if msg != -1:
                            selapot = msg
                            # self.queue1.put(-1)
                            print("------ 最高点 %.2f ------" % msg)
                    else:
                        if msg != -1:
                            selapot = msg
                            print("时间窗口最大值 %.2f" % selapot)
                        if (currentprice - selapot) >= 0:
                            # selapot = currentprice
                            continue
                        elif -0.02 < (currentprice - selapot) < 0:
                            print('第二次最高点确认当前价股价 %.2f' % currentprice)
                            self.queue1.put(-1)
                            t_times = datetime.datetime.now().strftime("%H:%M:%S")
                            break
                        else:
                            print('错过最高点，赶紧卖出')
                            self.queue1.put(-1)
                            t_times = datetime.datetime.now().strftime("%H:%M:%S")
                            break
        return code + "-" + str(currentprice) + "-" + str(count) + "-" + t_times

    def get_data(self, code):
        datas = ts.get_tick_data(code=code, date=config['trade']['simulate-day'], src=config['data_source'])
        prices = []
        t_time = []
        for index, data in datas.iterrows():
            # if index % 2 == 0:
            prices.append(data['price'])
            t_time.append(data['time'])
        return prices, datas[0:1].values[0][1], t_time


if __name__ == '__main__':
    # data = ts.get_realtime_quotes(symbols='603993')
    # datas = ts.get_tick_data(code='603993', date='2020-02-28', src='tt')
    print('s')
