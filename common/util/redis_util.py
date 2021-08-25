# coding:utf-8
import json

from redis import StrictRedis


class RedisUtil:

    def __init__(self):
        print('初始化连接redis')
        self.store = StrictRedis(host='localhost', port=6379, db=0)

    # 存储数据到redis
    def buy_save(self, codes):  # 存入到redis中
        json_encode = json.dumps(codes)
        self.store.zadd('buy_code', {json_encode: 5})
        # self.store.lpush(codes[0], json_encode)

    # 存储数据到redis
    def sela_save(self, codes):  # 存入到redis中
        json_encode = json.dumps(codes)
        self.store.zadd('sela_code', {json_encode: 5})
        # self.store.lpush(codes[0], json_encode)


redis = RedisUtil()
