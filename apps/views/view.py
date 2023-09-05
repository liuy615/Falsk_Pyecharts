# -*- coding: utf-8 -*
# @Time    : 2023/6/25 14:11
# @Author  : liuy
# @File    : view.py
import pandas as pd
from flask import render_template, Blueprint
from apps.views.draw import MonthFlow


# 1. 创建一个蓝图模板
view_bule = Blueprint("view", __name__)


# 2. 定义视图函数，配置蓝图路由
@view_bule.route("/month_pv")
def index():
    month_flow = MonthFlow()
    month_flow.pv_data("apps/static/2月数据/month_flow_data.xlsx", "apps/templates/2月可视化/2018_2_pv.html")
    return render_template("2月可视化/month_pv.html")


@view_bule.route("/month_uv")
def index():
    month_flow = MonthFlow()
    month_flow.uv_data("apps/static/2月数据/month_flow_data.xlsx", "apps/templates/2月可视化/2018_2_uv.html")
    return render_template("2月可视化/month_uv.html")



