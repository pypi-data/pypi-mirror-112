# -*- coding: utf-8 -*-
# @author: leesoar

"""数据库操作

Usage:
    mysql = Mysql()

    sql = "select id, name from table_a"
    res = mysql.exec(sql)
    mysql.log.debug(res)
"""

import abc

import clickhouse_driver
import psycopg2
import pymongo
import pymysql
import redis

from ..util.base import extract
from ..util.decorator import mysql_dba, retry, bit_bucket
from ..util.logger import Logger


class BaseDb(object, metaclass=abc.ABCMeta):
    """各数据库操作的基类"""

    def __new__(cls, *args, **kwargs):
        """限制客户端实例创建，避免建立多个客户端连接"""
        if not hasattr(cls, 'inst'):
            cls.inst = super().__new__(cls)
        return cls.inst

    def __init__(self):
        self.log = Logger(f"{__name__}.log").get_logger()


class Mysql(BaseDb):
    """MySQL的操作类"""

    def __init__(self, _config):
        super().__init__()
        self._config = _config
        self._conn = None
        self._cursor = None

    def _connect(self):
        return pymysql.connect(**self._config)

    def set_config(self, cfg):
        self._config = cfg

    @retry()
    @mysql_dba
    def exec(self, sql, data=None, is_dict=False):
        """执行sql

        对数据库的操作，返回元组、字典或None

        Usage:
            sql = "insert ignore into table_a(uid, name) values(%s, %s)"
            data = {"uid": "888", "name": "leesoar"}
            # or data = ["888", "leesoar"]
            # or data = ("888", "leesoar")
            mysql.exec(sql, data=data)
        Args:
            sql: 数据库语句(DDL, DML等)
            data: 插入时使用，默认为None。类型可为list, tuple, dict
            is_dict: 确定返回结果的类型。默认为False，即返回元组
        Returns:
            执行结果。tuple, dict or None
        """
        with self._conn.cursor(is_dict and pymysql.cursors.DictCursor) as cursor:
            self._cursor = cursor
            self._cursor.execute(sql, data)
            result = cursor.fetchall()
        return result

    @retry()
    @mysql_dba
    def exec_many(self, sql, data=None, is_dict=False):
        """执行sql

        对数据库的操作，返回元组、字典或None

        Usage:
            sql = "insert ignore into table_a(uid, name) values(%s, %s)"
            data = {"uid": "888", "name": "leesoar"}
            # or data = ["888", "leesoar"]
            # or data = ("888", "leesoar")
            mysql.exec(sql, data=data)
        Args:
            sql: 数据库语句(DDL, DML等)
            data: 插入时使用，默认为None。类型可为list, tuple, dict
            is_dict: 确定返回结果的类型。默认为False，即返回元组
        Returns:
            执行结果。tuple, dict or None
        """
        with self._conn.cursor(is_dict and pymysql.cursors.DictCursor) as cursor:
            self._cursor = cursor
            self._cursor.executemany(sql, data)
            result = cursor.fetchall()
        return result


class PostgreSql(BaseDb):
    """PostgreSQL的操作类"""

    def __init__(self, _config):
        super().__init__()
        self._config = _config

    def _connect(self):
        return psycopg2.connect(**self._config)

    def set_config(self, cfg):
        self._config = cfg

    @retry()
    def insert(self, *data, schema, table, conflict: tuple, do=None):
        """基础insert"""
        fields = extract(data).keys()

        if isinstance(do, (tuple, list)):
            do = f"update set {', '.join(map(lambda x: f'{x}=excluded.{x}', do))}"
        elif not do:
            do = "nothing"

        sql = f"""
            insert into {schema}.{table} ({", ".join(fields)})
            values ({", ".join(map(lambda x: f"%({x})s", fields))})
            on conflict({", ".join(conflict)})
            do {do}
        """
        self.exec(sql, *data)

    @retry()
    def exec(self, sql, *args):
        """执行sql"""
        conn = self._connect()
        try:
            with conn:
                with conn.cursor() as cursor:
                    if len(args) == 0:
                        cursor.execute(sql)
                    elif len(args) != 1:
                        cursor.executemany(sql, args)
                    else:
                        cursor.execute(sql, *args)

                    try:
                        ret = cursor.fetchall()
                    except psycopg2.ProgrammingError:
                        ret = None
        except Exception as e:
            self.log.debug(f"【捕获到异常】{sql}\n\t{e}")
        else:
            return ret
        finally:
            conn.close()


class ClickHouse(BaseDb):
    """ClickHouse的操作类"""

    def __init__(self, _config):
        super().__init__()
        self._config = _config
        self._client = self._connect()

    def _connect(self):
        return clickhouse_driver.Client(**self._config)

    @bit_bucket()
    @retry()
    def exec(self, sql, data=None):
        return self._client.execute(sql, data)


class Redis(BaseDb):
    """Redis的操作类"""

    def __init__(self, _config):
        super().__init__()
        self._conn = redis.Redis(connection_pool=self.__get_pool(_config))

    @staticmethod
    def __get_pool(_config):
        if isinstance(_config, dict):
            return redis.ConnectionPool(**_config)
        return redis.ConnectionPool.from_url(_config)

    def get_client(self):
        return self._conn


class Mongo(BaseDb):
    """Mongo的操作类"""

    def __init__(self, _config):
        super().__init__()
        self._config = _config
        self._client = self._connect()

    def _connect(self):
        if isinstance(self._config, dict):
            return pymongo.MongoClient(**self._config)
        return pymongo.MongoClient(self._config)

    @retry()
    def exec(self, data, *, database=None, collection=None):
        if None in [database, collection]:
            raise type("MongoConfigError", (Exception,), {})("need database and collection")

        if isinstance(data, dict):
            return self._client[database][collection].insert_one(data)
        return self._client[database][collection].insert_many(data)


if __name__ == "__main__":
    pass
