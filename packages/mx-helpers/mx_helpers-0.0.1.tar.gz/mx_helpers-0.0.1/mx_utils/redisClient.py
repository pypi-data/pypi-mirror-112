# -*- coding: utf-8 -*-
# @Time    : 2021/6/8 3:00 下午
# @Author  : X.Lin
# @Email   : ****
# @File    : redisClient.py
# @Software: PyCharm
# @Desc    : Redis客户端

import redis
import importlib
import json

class List(object):

    def __init__(self, redis: 'redis.client.Redis'):
        self._redis = redis

    def pop(self, key: str, block: bool = True):
        """
        弹出一个元素, `阻塞`
        :param block:
        :return:
        """
        if block:
            return self._redis.blpop(key)[1]
        else:
            try:
                return self._redis.lpop(key)
            except:
                return None

    def push(self, key: str, item):
        return self._redis.lpush(key, json.dumps(item)) != 0

class RedisClient():

    def __init__(self, config: dict):
        """
        init
        :param config:
            {
                "host": "127.0.0.1",
                "password": "",
                "port": 6379,
                "db": 0,
            }
        """
        self._config = config

        # ----- load config
        host = config.get("host", "127.0.0.1")
        password = config.get("password", "")
        port = config.get("port", 6379)
        db = config.get("db", 0)
        # ----- init redis ins ...
        self._pool = redis.ConnectionPool(host=host, password=password, port=port, db=db, decode_responses=True)
        self._redis = redis.Redis(connection_pool=self._pool)

    def __getattr__(self, item: str):
        """本函数用于获取各种类，如 `List` `RSet` 等.

        :支持的形式有:
            1. client.List()
            2. client.RSet()
        """

        def getter():
            return eval(item.capitalize())(redis=self._redis)

        attr_list = ['list', 'set']
        if item.lower() in attr_list:
            return getter

