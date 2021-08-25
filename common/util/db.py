# -*- coding: UTF-8 -*-

import pymysql


class DataSource:

    def __init__(self):
        # 首先导入email模块构造邮件
        self.db = pymysql.connect(host='127.0.0.1', user='root', passwd=' ', port=3306, db='share', charset='utf8')
        self.cur = self.db.cursor()

    def modify(self, tablename):
        sql = "alter table ...."
        try:
            # 如果数据表已经存在使用 execute() 方法删除表。
            # self.cur.execute("DROP TABLE IF EXISTS `" + tablename + "`")
            # 执行sql语句
            self.cur.execute(sql)
            self.db.commit()
        except:
            print('修改表: ' + tablename + '错误')
        return False

    # 创建表
    def create(self, tablename):
        if self.checkexist(tablename):
            return True
        # 创建数据表SQL语句
        sql = "CREATE TABLE  `" + tablename + "`"
        print(sql)
        try:
            # 如果数据表已经存在使用 execute() 方法删除表。
            # self.cur.execute("DROP TABLE IF EXISTS `" + tablename + "`")
            # 执行sql语句
            self.cur.execute(sql)
            self.db.commit()
        except:
            print('创建表: ' + tablename + '错误')
        return False

    # 新增数据
    def insert(self, sql):
        # SQL 插入语句
        try:
            # 执行sql语句
            self.cur.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # Rollback in case there is any error
            self.db.rollback()

    # 删除数据
    def delete(self, sql):
        try:
            # 执行sql语句
            print(sql)
            self.cur.execute(sql)
            self.db.commit()
            # 提交到数据库执行
        except:
            # Rollback in case there is any error
            self.db.rollback()

    # 查询数据
    def select(self, sql):
        try:
            # 执行sql语句
            self.cur.execute(sql)
            return self.cur.fetchall()
        except:
            print('查询数据库错误: ' + sql)

    # 执行sql不反回数据
    def excute(self, sql):
        try:
            print(sql)
            # 执行sql语句
            self.cur.execute(sql)
            self.db.commit()
        except:
            print('查询数据库错误: ' + sql)
            self.db.rollback()

    # 判断表是否存在
    def checkexist(self, tablename):
        try:
            sql = """desc `""" + tablename + """`;"""
            # print(sql)
            self.cur.execute(sql)
            flag = True
        except:
            flag = False
        return flag

    # 关闭数据库
    def close(self):
        self.db.close()
