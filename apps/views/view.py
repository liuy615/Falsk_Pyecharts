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
@view_bule.route("/month_pv")
def month_flow_pv():
    month_flow = MonthFlow()
    month_flow.pv_data("apps/static/2月数据/month_pv_data.xlsx", "apps/static/3月数据/month_pv_data.xlsx", "apps/templates/3月可视化/2018_3_pv.html")
    return render_template("3月可视化/2018_3_pv.html")


@view_bule.route("/month_uv")
def month_flow_uv():
    month_flow = MonthFlow()
    month_flow.uv_data("apps/static/2月数据/month_uv_data.xlsx", "apps/static/3月数据/month_uv_data.xlsx", "apps/templates/3月可视化/2018_3_uv.html")
    return render_template("3月可视化/2018_3_uv.html")


@view_bule.route("/")
def index():

    return render_template("index.html")


@view_bule.route("/json")
def index_data():
    print("进来了")
    # data_json = {}
    # data1 = [683, 234, 234, 523, 345, 320, 280, 271, 254, 229, 210, 190, 182]
    # data_json["data1"] = data1
    # data2 = ['北京', '上海', '广州', '郑州', '武汉', '南京', '杭州', '东莞', '深圳', '虎门', '青岛', '石家庄', '安阳']
    # data_json["data2"] = data2
    data = {"leixing": ['北京', '上海', '广州', '郑州', '武汉', '南京', '杭州', '东莞', '深圳', '虎门', '青岛', '石家庄', '安阳'], "num": [683, 234, 234, 523, 345, 320, 280, 271, 254, 229, 210, 190, 182]}
    data1 = pd.DataFrame(data)
    data2 = data1.to_dict(orient="list")
    return jsonify(data2)
    # return Response(json.dumps(data_json), mimetype='application/json')










@view_bule.route("/2")
def index2():

    return render_template("index2.html")


@view_bule.route("/json2")
def data2():
    print("进来了")
    data = {"类型": ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'], "数量": [5, 20, 36, 10, 10, 20]}
    data1 = pd.DataFrame(data)
    data2 = data1.to_dict(orient="list")
    return jsonify(data2)