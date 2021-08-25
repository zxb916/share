# coding:utf-8

import pandas as pd
from sqlalchemy import create_engine
import tushare as ts
from common.util.date_util import DateUtil
from common.util.db import DataSource


class TuUtil:
    # 初始化
    def __init__(self):
        token = ''
        self.pro = ts.pro_api(token)
        self.dateutil = DateUtil()
        self.stock = DataSource()
        # 将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
        self.yconnect = create_engine('mysql+mysqldb://root:pwd@localhost:3306/share?charset=utf8')

    def get_stock_list(self):
        return self.pro.stock_basic(exchange='', list_status='L',
                                    fields='ts_code,symbol,name,area,industry,list_date,market')

    def create_or_update_table(self, data, table_name):
        pd.io.sql.to_sql(data, table_name, self.yconnect, schema='share', if_exists='append')

    def get_company_info(self):
        # 上市公司基本信息 SSE上交所 SZSE深交所 ，默认SSE
        return self.pro.stock_company(exchange='SSE',
                                      fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,'
                                             'province,employees,main_business,business_scope')

    # 只获取数据不存表
    def insert_code_list(self):
        # tu = TuUtil()
        # tu.manual_update_sub('2020-4-13')
        # print('test')
        df = self.get_stock_list()
        self.stock.excute('drop table today')
        self.create_or_update_table(df, 'today')
        self.stock.excute('DELETE from today where market="科创板"')
        print("success")


if __name__ == '__main__':
    # tu = TuUtil()
    # tu.manual_update_sub('2020-4-13')
    # print('test')
    # df = tu.get_stock_list()
    # tu.create_or_update_table(df, 'today')
    # tu.stock.dbutil.excute('DELETE from today where market="科创板"')
    print("success")
