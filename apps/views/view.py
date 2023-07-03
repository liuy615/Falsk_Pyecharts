# -*- coding: utf-8 -*
# @Time    : 2023/6/25 14:11
# @Author  : liuy
# @File    : view.py
import pandas as pd
from flask import render_template, Blueprint
from apps.views.draw import flow_data


# 1. 创建一个蓝图模板
view_bule = Blueprint("view", __name__)


# 2. 定义视图函数，配置蓝图路由
@view_bule.route("/")
def index():
    flow_data("apps/static/3月数据/month_flow_data.xlsx", "apps/templates/html/month_flow_data.html")
    return render_template("html/month_flow_data.html")


