# -*- coding: utf-8 -*
# @Time    : 2023/6/25 15:11
# @Author  : liuy
# @File    : tools.py
import pymysql
import pandas as pd
from pyecharts.charts import Line, Bar
from pyecharts import options as opts


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


# 1. 流量分析
data = pd.read_pickle("../static/data/data_action_march.pkl")
data1 = pd.read_pickle("../static/data/data_action.pkl")


# 1.1.1 PV日流量数据准备
def pv_day_group():
    data1["day"] = data1["date"].dt.day
    data1["month"] = data1["date"].dt.month
    data1_group = data1.groupby(["day", "month"]).agg(平均数=("user_id", "count")).reset_index()
    d1 = round(data1_group.groupby("day")["平均数"].mean())
    data_d1 = [i for i in d1]
    data["day"] = data["date"].dt.day
    date_group = data.groupby("day").agg(人数=("user_id", "count")).reset_index()
    data_xaxis = [str(i) for i in date_group["day"]]
    data_yaxis = date_group["人数"].tolist()

    # 画图
    line = (
        Line()
        .add_xaxis(data_xaxis)
        .add_yaxis("人数", data_yaxis, label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis("平均值", data_d1, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="2月PV流量分析"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            xaxis_opts={"min": data_xaxis[0]}
        )
    )
    return line


# 1.1.2 PV周流量数据准备
def pv_week_group():
    data["week"] = data["date"].dt.day_name()
    data_group = data.groupby("week").agg(人数=("week", "count")).sort_values("人数", ascending=False)
    data_xaxis = data_group["week"].tolist()
    data_yaxis = data_group["人数"].tolist()
    # 画图
    bar = (
        Bar()
        .add_xaxis(data_xaxis)
        .add_yaxis("人数", data_yaxis, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts("PV周流量折线图")
        )
    )
    return bar


# 1.1.3 PV时流量数据准备
def pv_hour_group():
    data["hour"] = data["action_time"].dt.hour
    data_group = data.groupby("hour").agg(人数=("hour", "count")).reset_index()
    data_xaxis = data_group["hour"].tolist()
    data_yaxis = data_group["人数"].tolist()
    # 画图
    bar = (
        Bar()
        .add_xaxis(data_xaxis)
        .add_yaxis("人数", data_yaxis, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts("PV时流量折线图")
        )
    )
    return bar


bar = pv_day_group()
bar.render("../templates/html/2月PV日流量分析.html")














if __name__ == '__main__':
    print("程序结束！")
