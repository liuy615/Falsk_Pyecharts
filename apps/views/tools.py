# -*- coding: utf-8 -*
# @Time    : 2023/6/25 15:11
# @Author  : liuy
# @File    : tools.py
import pymysql
import pandas as pd


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


def get_rate_increase(last_data, data):
    rate_data = pd.concat([last_data, data], axis=1, ignore_index=True)
    rate_data["rate"] = round((rate_data[3] - rate_data[1]) / rate_data[1]*100, 2)
    return rate_data["rate"]


if __name__ == '__main__':
    print("程序结束！")
