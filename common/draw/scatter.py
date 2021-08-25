# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd

import numpy as np

plt.rcParams["font.sans-serif"] = ['SimHei']  # 用来正常显示中文标签，SimHei是字体名称，字体必须在系统中存在，字体的查看方式和安装第三部分
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

if __name__ == '__main__':
    # 预未来几天天涨跌幅测试天数
    data = pd.read_csv('000001.csv', index_col=0)
    data = data[-1000:]
    data['open'] = data.apply(lambda x: (x.open - x.pre_close) / x.pre_close * 100, axis=1)
    data['high'] = data.apply(lambda x: (x.high - x.pre_close) / x.pre_close * 100, axis=1)
    data['low'] = data.apply(lambda x: (x.low - x.pre_close) / x.pre_close * 100, axis=1)
    data['close'] = data.apply(lambda x: (x.close - x.pre_close) / x.pre_close * 100, axis=1)

    data['new'] = np.where(data['pct_chg'] >= 2, 2, np.where(data['pct_chg'] >= 1, 1, 0))
    features = ['open', 'high', 'low', 'close', 'new']
    data = data[features]
    X1 = data.iloc[:, :2].values
    y = data['new'].values
    print(type(y[0]))
    plt.scatter(X1[y == 0, 0], X1[y == 0, 1], color='r', marker='+')  # 选取y所有为0的+X的第一列
    plt.scatter(X1[y == 1, 0], X1[y == 1, 1], color='g', marker='x')  # 选取y所有为1的+X的第一列
    plt.scatter(X1[y == 2, 0], X1[y == 2, 1], color='b', marker='o')  # 选取y所有为2的+X的第一列

    plt.xlabel('sepal width')  # 设置横坐标标注xlabel为sepal width
    plt.ylabel('sepal length')  # 设置纵坐标标注ylabel为sepal length
    plt.title('sepal散点图')  # 设置散点图的标题为sepal散点图
    plt.show()
