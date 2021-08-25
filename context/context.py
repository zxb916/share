# -*- coding: utf-8 -*-


class BuyContext(object):

    def __init__(self, buy_stock):
        self.buy_stock = buy_stock

    def set(self, param):
        self.buy_stock = param

    def buy(self, code):
        self.buy_stock.buy(code)
