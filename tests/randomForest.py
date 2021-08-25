# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


def testStock():
    # 测试天数
    day = 1
    # 样本数据
    df = pd.read_csv('000001.SZ.csv')
    df['open'] = df.apply(lambda x: (x.open - x.pre_close) / x.pre_close * 100, axis=1)
    df['high'] = df.apply(lambda x: (x.high - x.pre_close) / x.pre_close * 100, axis=1)
    df['low'] = df.apply(lambda x: (x.low - x.pre_close) / x.pre_close * 100, axis=1)
    df['close'] = df.apply(lambda x: (x.close - x.pre_close) / x.pre_close * 100, axis=1)
    df = df[
        ['open', 'high', 'low', 'close', 'vol', 'pct_chg']]
    price = []
    for num in range(1, len(df) - day):
        temp = 0.0
        for i in range(0, day):
            temp = temp + float(df['pct_chg'].values[num + i])
        price.append(temp)

    df = df[:-1 - day]
    df['price'] = price
    # 后一天是1 今天就为1
    df['pre'] = np.where(df['price'] >= 1, 1, 0)
    # df.to_csv("data/000001.csv")
    split = int(len(df) * 0.9)
    train = df[:split]
    test = df[split:].copy()
    # 特征选取
    features = df.columns.values.tolist()[:-2]
    clf = RandomForestClassifier(n_jobs=4)
    y = train['pre'].values.tolist()
    # print(y)
    # 训练集数据 和 结果
    clf.fit(train[features], y)  # 用train来训练样本
    test_pred = clf.predict(test[features])  # 用测试数据来做预测
    print(type(test_pred))
    # submission = pd.DataFrame({'RISK': test_pred})
    test['actual'] = test_pred
    t = test['pre'].values.tolist()
    test.to_csv('test.csv')
    print(classification_report(t, test_pred))
    # result = pd.crosstab(t, test_pred, rownames=['actual'], colnames=['pre'])
    # print(result)
    joblib.dump(clf, "000004.m")
    # clf = joblib.load("train_model.m")


testStock()
