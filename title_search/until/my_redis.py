# -*- coding: UTF-8 -*-
# @author: ylw
# @file: my_redis
# @time: 2022-4-13
# @desc:
import redis
from settings import REDIS_CONNECT
from loguru import logger
import traceback
import sys


class RedisClient:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            return object.__new__(cls)
        return cls.__instance

    def __init__(self, db, max_connections):
        try:
            # 拿到一个Redis实例的连接池，避免每次建立、释放连接的开销，节省了每次连接用的时间
            self.POLL = redis.ConnectionPool(host=REDIS_CONNECT['host'],
                                             port=REDIS_CONNECT['port'],
                                             db=db,
                                             password=REDIS_CONNECT['password'],
                                             decode_responses=True,
                                             max_connections=max_connections)
        except Exception as e:
            logger.error(f'获取Redis连接池异常, 程序退出:{str(e)},traceback={traceback.format_exc()}')
            sys.exit(0)

    def get_redis_client(self):
        try:
            # 从连接池中获取一个连接实例
            redis_conn = redis.StrictRedis(connection_pool=self.POLL)
            if redis_conn.ping():
                logger.info(f'获取Redis连接实例成功')
            return redis_conn
        except Exception as e:
            logger.error(f'Redis连接异常:{str(e)},traceback={traceback.format_exc()}')


class Redis_util(RedisClient):
    """
    redis数据库的常用操作
    """

    def __init__(self, db, max_connections):
        super(Redis_util, self).__init__(db, max_connections)
        self.db = self.get_redis_client()

    def S_add(self, table_name, value):
        """
        向集合添加元素
        :param table_name: 集合名
        :param value:元素
        :return:
        """
        return self.db.sadd(table_name, value)

    def S_pop(self, table_name=None):
        """
        随机返回并删除名称为key的set中一个元素
        :param table_name:
        :return:
        """
        return self.db.spop(table_name)

    def S_len(self, table_name=None):
        """
        返回名称为key的set的基数
        :param table_name:
        :return:
        """
        return self.db.scard(table_name)

    def S_isMember(self, table_name, value):
        """
        member是否是名称为key的set的元素
        :param table_name:
        :param value:
        :return:
        """
        return self.db.sismember(table_name, value)

    def L_push(self, table_name, value):
        """
        在名称为key的list头添加一个值为value的 元素
        :param table_name:
        :param value:
        :return:
        """
        return self.db.lpush(table_name, value)

    def L_pop(self, table_name=None):
        """
        返回并删除名称为key的list中的首元素
        :param table_name:
        :return:
        """
        return self.db.lpop(table_name)

    def L_rpop(self, table_name=None):
        """
        返回并删除名称为key的list中的尾元素
        :param table_name:
        :return:
        """
        return self.db.rpop(table_name)

    def L_len(self, table_name=None):
        """
        返回名称为key的list的长度
        :param table_name:
        :return:
        """
        return self.db.llen(table_name)

    def H_set(self, id, value, table_name=None):
        """
        向名称为key的hash中添加元素field
        :param id:
        :param value:
        :param table_name:
        :return:
        """
        return self.db.hset(table_name, id, value)

    def H_get(self, key, table_name=None):
        """
        返回名称为key的hash中field对应的value
        :param key:
        :param table_name:
        :return:
        """
        return self.db.hget(table_name, key=key)

    def H_getAll(self, table_name=None):
        """
        返回名称为key的hash中所有的键（field）及其对应的value
        :param table_name:
        :return:
        """
        return self.db.hgetall(table_name)

    def H_keys(self, table_name=None):
        """
        返回名称为key的hash中所有键
        :param table_name:
        :return:
        """
        return self.db.hkeys(table_name)

    def H_del(self, key, table_name=None):
        """
        删除名称为key的hash中键为field的域
        :param key:
        :param table_name:
        :return:
        """
        return self.db.hdel(table_name, key)

    def H_len(self, table_name=None):
        """
        返回名称为key的hash中元素个数
        :param table_name:
        :return:
        """
        return self.db.hlen(table_name)

    def Del_(self, table_name=None):
        """
        删除
        :param table_name:
        :return:
        """
        return self.db.delete(table_name)

    def S_rem(self, table_name, value):
        """
        删除名称为key的set中的元素member
        :param table_name:
        :param value:
        :return:
        """
        return self.db.srem(table_name, value)


if __name__ == '__main__':
    # a = Redis_util(1, 10)
    # b = a.S_add('ceshi', 1)
    # print(b)
    from retry import retry


    @retry(tries=2,)
    def func():
        print('开始')
        print('1'+1)

    func()
