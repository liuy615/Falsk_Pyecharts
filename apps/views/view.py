# -*- coding: utf-8 -*
# @Time    : 2023/6/25 14:11
# @Author  : liuy
# @File    : view.py
import json

import pandas as pd
from flask import render_template, Blueprint, jsonify, Response
from apps.views.draw import MonthFlow


# 1. 创建一个蓝图模板
view_bule = Blueprint("view", __name__)


# 2. 定义视图函数，配置蓝图路由
# echarts主页
@view_bule.route("/")
def index():

    return render_template("index.html")


# month_pv页面
@view_bule.route("/month_pv")
def month_flow_pv():
    month_flow = MonthFlow()
    month_flow.pv_data("apps/static/2月数据/month_pv_data.xlsx", "apps/static/3月数据/month_pv_data.xlsx", "apps/templates/3月可视化/2018_3_pv.html")
    return render_template("3月可视化/2018_3_pv.html")


# month_uv页面
@view_bule.route("/month_uv")
def month_flow_uv():
    month_flow = MonthFlow()
    month_flow.uv_data("apps/static/2月数据/month_uv_data.xlsx", "apps/static/3月数据/month_uv_data.xlsx", "apps/templates/3月可视化/2018_3_uv.html")
    return render_template("3月可视化/2018_3_uv.html")


# data_csv是以下几个图共同使用的数据，这里只读一遍，加快加载速度
data_csv = pd.read_csv("apps/static/data/data_user.csv")


# echarts左二可视化图示数据
@view_bule.route("/l2")
def echarts_l2():
    print("l2")
    data_age = data_csv["age"].value_counts()
    data = {"类型": data_age.index.tolist(), "数量": data_age.tolist()}
    return jsonify(data)


# echarts中二可视化图示数据
@view_bule.route("/c2")
def echarts_c2():
    print("每日销售数据")
    data_csv["year"] = pd.to_datetime(data_csv["user_reg_tm"]).dt.year
    data_reg_time = data_csv["year"].value_counts(sort=False).sort_index()
    data = {"日期": data_reg_time.index.tolist(), "num": data_reg_time.tolist()}
    return jsonify(data)


# echarts右1可视化图示数据
@view_bule.route("/r1")
def echarts_r1():
    print("r1")
    data_city_level = data_csv["city_level"].value_counts().sort_index().tolist()
    data_city_level.insert(0, sum(data_city_level))
    city_level = ["总共", "未知", "一线城市", "二线城市", "三线城市", "四线城市", "五线城市", "六线城市"]
    city_none, data_none = [0, ], 0
    for x in data_city_level[1:]:
        data_none += x
        data = data_city_level[0] - data_none
        city_none.append(data)
    data = {"city_level": city_level, "city_none": city_none, "data_city_level": data_city_level}
    return jsonify(data)


# echarts右2可视化图示数据
@view_bule.route("/r2")
def echarts_r2():
    print("r2")
    sex_data = pd.DataFrame(data_csv["sex"].value_counts())
    data = {str(key): int(value["sex"]) for key, value in sex_data.iterrows()}
    return jsonify(data)


# echarts右3可视化图示数据
@view_bule.route("/r3")
def echarts_r3():
    print("r3")
    user_lv_cd = data_csv.groupby(by="user_lv_cd")["user_id"].count().to_list()
    data = {"num": user_lv_cd}
    return jsonify(data)
