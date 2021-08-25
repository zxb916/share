# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tushare as ts

if __name__ == '__main__':
    datas = ts.get_hist_data(code="600031")
    # datas = datas.sort_values(by="date", ascending=True)
    low_spot = datas['turnover'].min()
    high_spot = datas['turnover'].max()
    print(high_spot)
    print(low_spot)
    turnovers = []
    t_time = []
    for index, data in datas.iterrows():
        # if index % 2 == 0:
        turnovers.append(data['turnover'])
        t_time.append(index)

    plt.plot(t_time, turnovers, color='g')
    plt.xlabel('time')
    plt.ylabel('volume')
    plt.show()
