# coding:utf-8
from threading import Thread
import time


# 多线程共享时用
# all_data = list()


class SelaAnalyze(Thread):

    def __init__(self, count, queue1, queue2):
        super().__init__()
        self.count = count
        self.data = list()
        self.queue1 = queue1
        self.queue2 = queue2
        # all_data.append(name)

    def run(self):
        self.time_window()

    # 时间窗口策略 通用
    def time_window(self):
        while True:
            # 阻塞程序，时刻监听
            msg = self.queue1.get()
            if msg == -1:
                break
            self.data.append(msg)
            # print("收到的消息 %.2f " % msg)
            # 一旦发现满足条件
            if len(self.data) == self.count:
                self.data.sort(reverse=True)
                tmp = self.data[0]
                self.data.clear()
                self.queue2.put(tmp)
            else:
                self.queue2.put(-1)
            # time.sleep(0.01)
        print('分析线程结束')
