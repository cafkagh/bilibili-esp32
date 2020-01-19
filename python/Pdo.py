# -*- coding: utf-8 -*-
import pymysql as mysql
import sqlite3


class Pdo:
    # 初始化连接
    def __init__(self, dbtype="", host="127.0.0.1", user="root", password="root", database="", charset="utf8", port=3306):
        try:
            # if(dbtype=="mysql"):
            #     self.connect = mysql.connect(host=host, user=user, password=password, database=database, harset=charset)
            #     self.cursor = self.connect.cursor()
            # else:
            self.connect = sqlite3.connect(database)
            self.cursor = self.connect.cursor()
        except Exception as e:
            print("数据库连接失败！")
            exit(e)

    # 根据where生成查询条件
    @staticmethod
    def build_where(where=""):
        if where == "":
            sql = "1=1"
        elif isinstance(where, dict):
            sql = where
        elif isinstance(where, str):
            sql = where

        else:
            sql = where
        return sql

    @staticmethod
    def build_order(order=""):
        if order!="":
            return " order by "+order
        else:
            return ""

    # 查询单条数据 返回dist
    def find(self, table, where='', field='*', order=''):
        data = {}
        where_sql = self.build_where(where)
        order_sql = self.build_order(order)
        sql = "select %s from %s where %s %s limit 0,1" % (field, table, where_sql, order_sql)
        try:
            self.cursor.execute(sql)
            cols = [tuple[0] for tuple in self.cursor.description]
            result = list(reversed(self.cursor.fetchone()))
            for col in cols:
                data[col.encode("utf-8")] = result.pop()
        except Exception as e:
            print("数据查询错误")
            print(e)
            self.connect.rollback()
        finally:
            # self.connect.close()
            return data

    # 查询多条数据 返回list
    def select(self, table, where='', field='*'):
        data = []
        where_sql = self.build_where(where)
        sql = "select %s from %s where %s" % (field, table, where_sql)
        print(sql)
        try:
            self.cursor.execute(sql)
            cols = [tuple[0] for tuple in self.cursor.description]
            results = self.cursor.fetchall()
            for result in results:
                r_result = list(reversed(result))
                line = {}
                for col in cols:
                    line[col.encode("utf-8")] = r_result.pop()
                data.append(line)
        except Exception as e:
            print("数据查询错误")
            print(e)
            # self.connect.rollback()
            data = {}
        finally:
            if field != '*' and ((',' in field) == False):
                lines = []
                for line in data:
                    lines.append(line[field])
                return lines
            else:
                return data

    # 删除一条
    def delete(self, table, where=''):
        where_sql = self.build_where(where)
        sql = "delete from %s where %s order by id desc limit 1" % (table, where_sql)
        try:
            result = self.cursor.execute(sql)
            self.connect.commit()
            return result
        except Exception as e:
            print("数据删除失败！")
            self.connect.rollback()
            return False

    # 删除多条
    def deleteAll(self, table, where=''):
        where_sql = self.build_where(where)
        sql = "delete from %s where %s" % (table, where_sql)
        try:
            result = self.cursor.execute(sql)
            self.connect.commit()
            return result
        except Exception as e:
            print("数据删除失败！")
            self.connect.rollback()
            return False

    # 查询数量
    def count(self, table, where='1=1'):
        where_sql = self.build_where(where)
        sql = 'select count(*) from `%s` where %s ' % (table, where_sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results[0][0]

    # 插入数据 结构[{fieldname:value},····]
    def insert_db(self, table, data):
        if table == "" or len(data) == 0:
            return False
        keys = data[0].keys()
        sql_key = "`" + ("`,`".join(keys)) + "`"
        new_data = []
        for line in data:
            new_line = []
            for key in keys:
                if type(line[key]).__name__ == 'unicode':
                    new_line_data = line[key].encode("utf-8")
                elif type(line[key]).__name__ != 'str':
                    new_line_data = str(line[key])
                else:
                    new_line_data = line[key]

                new_line.append(new_line_data)
            new_data.append("'" + ("','".join(new_line)) + "'")
        sql_value = "(" + ("),(".join(new_data)) + ")"

        sql = "insert into `" + table + "`(" + sql_key + ") values " + sql_value
        # print(sql)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print("数据写入失败！"),
            print(e),
            print(sql)
            exit()
            self.connect.rollback()
            return False

    # 更新
    def save(self, table, where, data):
        new_data = []
        where_sql = self.build_where(where)
        for line in data:
            new_data.append(str(line) + " = " + str(data[line]))
        data_sql = " and  ".join(new_data)
        sql = "update %s set %s where %s" % (table, data_sql, where_sql)
        try:
            result = self.cursor.execute(sql)
            self.connect.commit()
            return result
        except Exception as e:
            print("数据更新失败！")
            self.connect.rollback()
            return False



if __name__ == "__main__":
    pdo = Pdo(host="127.0.0.1", user="root", password="root", database="kuaixun", charset="utf8")
