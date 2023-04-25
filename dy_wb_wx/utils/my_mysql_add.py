# -*- coding: UTF-8 -*-
# @author: ylw
# @file: testmysql1.0
# @time: 2022-4-14
# @desc:
import pymysql
from dbutils.pooled_db import PooledDB
import time
from settings import MYSQL_INFO, mysql_info, content_table
import datetime
from loguru import logger

from settings import mysql_info, run_time




class MySql(object):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            return object.__new__(cls)
        return cls.__instance

    __pool = None

    def __init__(self, MYSQL_INFO_=MYSQL_INFO, content_table_=content_table):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        self.MYSQL_INFO = MYSQL_INFO_
        self.content_table = content_table_
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()

    def __getConn(self):
        """
        @return MySQLdb.connection
        """
        if MySql.__pool is None:
            MAX = 100
            __pool = PooledDB(
                pymysql,
                MAX,
                ping=1,
                host=self.MYSQL_INFO['host'],
                port=self.MYSQL_INFO['port'],
                user=self.MYSQL_INFO['user'],
                passwd=self.MYSQL_INFO['password'],
                db=self.MYSQL_INFO['db'],
                autocommit=True)
        else:
            return None
        return __pool.connection()

    def getAll(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def getOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertOne(self, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        # self._cursor.ping(reconnect=True)
        return self._cursor.execute(sql, value)
        # return self.__getInsertId()

    def updateOne(self, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        # self._cursor.ping(reconnect=True)
        return self._cursor.execute(sql, value)
        # return self.__getInsertId()

    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    # def __getInsertId(self):
    #     """
    #     获取当前连接最后一次插入操作生成的id,如果没有则为０
    #     """
    #     self._cursor.execute("SELECT @@IDENTITY AS id")
    #     result = self._cursor.fetchall()
    #     return result[0]['id']

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """

        return self.__query(sql, param)

    def delete(self, item, yesterday_start_time, yesterday_end_time):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        # keys = ', '.join(item.keys())
        # values = ', '.join(['%s'] * len(item))
        sql = f"""DELETE from  {self.content_table} where news_id = {item}  and create_time BETWEEN {yesterday_start_time} and {yesterday_end_time} """
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            # logger.info('入库成功')
            return True
        except Exception as e:
            # if '1062' in str(e):
            #     logger.info(f"入库失败----> {item['video_url']}")
            #     return True
            # else:
            self._conn.rollback()
            print("删除失败")
            logger.info(f"入库失败---->{e}")
            return False

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback');
        self._cursor.close()
        self._conn.close()

    def insert(self, item):
        """
        插入数据库
        :param item:
        :return:
        """
        keys = ', '.join(item.keys())
        values = ', '.join(['%s'] * len(item))
        sql_1 = f"""insert into {self.content_table} ({keys}) values ({values})"""
        try:
            self.insertOne(sql_1, tuple(item.values()))
            self.end()
            logger.info('入库成功')
            return True
        except Exception as e:
            # if '1062' in str(e):
            #     logger.info(f"入库失败----> {item['video_url']}")
            #     return True
            # else:
            logger.info(f"入库失败---->{e}")
            return False


if __name__ == '__main__':
    # __conn = MySql(mysql_info)
    #     sql = f'''SELECT video_url from sys_video_hot_search where video_url = "https://www.ixigua.com/7113354350973420064?utm_source=xigua_hotspot&category_name=subv_xg_hotspot&enter_from=click_hotspot&groupid=7113354350973420064"'''
    #     result = __conn.getOne(sql)
    #     if result:
    #         print(result)
    #         print('************')
    #     else:
    #         print('AAAAAAAAAAAAAAAAAA')
    # sql = f"""select reg_id from sys_wx_news where id =1"""
    # results = __conn.getOne(sql)
    # print(results)
    items = {
        'dsads': 1,
        'cdsfd': 2
    }
    item2 = {
        'dsads': 3,
        'cdsfd': 4
    }
    item_list = [items, item2]
    print(','.join(item_list[1].keys()))
    print(str([tuple(['%s'] * len(a.values())) for a in item_list])[1:-1].replace("'", ''))
    print(tuple(items.values()))
    print(', '.join(['%s'] * len(items)))
