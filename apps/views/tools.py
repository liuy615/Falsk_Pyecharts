# -*- coding: utf-8 -*
# @Time    : 2023/6/25 15:11
# @Author  : liuy
# @File    : tools.py
import pymysql


# 连接数据库
def get_con():
    """
    获取MySql连接，return：mysql connection
    """
    return pymysql.connect(host="127.0.0.1",
                           user="root",
                           password="513921",
                           database="jd_data",
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


# 进行数据查询
def get_query(sql):
    """
    根据SQL代码进行查询，并返回结果 paramater SQL
    return str
    """
    conn = get_con()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return list(cursor.fetchall())
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    print("程序结束！")
