# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, Response
import json
from service import tradeservice
from context.buystock import LowPrice, AmHalfNine, PmHalfTwo, BuyTest

'''
 flask: seb框架，通过flask提供的装饰器@server.route()将普通函数转换为服务　
 登录接口，需要传入url,username,passwd
'''
app = Flask(__name__)


# 跨域支持
# def after_request(resp):
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp
#
#
# app.after_request(after_request)


# @app.after_request
# def cors(environ):
#     environ.headers['Access-Control-Allow-Origin'] = '*'
#     environ.headers['Access-Control-Allow-Method'] = '*'
#     environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
#     return environ


@app.route("/share/data", methods=['POST'])
def get_data():
    data = request.get_json()
    codes = data['code']
    response = Response(json.dumps({'返回结果': tradeservice.get_data(codes)}), mimetype='application/json')
    return response


@app.route("/share/low_price_buy", methods=['POST'])
def low_price_buy():
    data = request.form.getlist('code')
    print(data)
    tradeservice.buy(LowPrice(), data[0])
    return 'success'


@app.route("/share/am_half_nine_buy", methods=['POST'])
def am_nine_buy():
    data = request.form.getlist('code')
    print(data)
    tradeservice.buy(AmHalfNine(), data[0])
    return 'success'


@app.route("/share/pm_half_two_buy", methods=['POST'])
def pm_half_buy():
    data = request.form.getlist('code')
    print(data)
    tradeservice.buy(PmHalfTwo(), data[0])
    return 'success'


@app.route("/share/sela", methods=['POST'])
def sela():
    data = request.form.getlist('code')
    print(data)
    tradeservice.sela(data[0])
    return 'success'


@app.route("/share/buy", methods=['POST'])
def buy():
    data = request.form.getlist('code')
    print(data)
    tradeservice.buy(BuyTest(), data[0])
    return 'success'


if __name__ == '__main__':
    # app.config['JSON_AS_ASCII'] = Falsec
    app.run(host='127.0.0.1', port='8080')
    app.run(debug=True)
