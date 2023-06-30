# -*- coding: utf-8 -*
# @Time    : 2023/6/25 14:11
# @Author  : liuy
# @File    : view.py
import pandas as pd
from flask import render_template, Blueprint
from apps.views.tools import get_query, pv_day_group


# 1. 创建一个蓝图模板
view_bule = Blueprint("view", __name__)


# 2. 定义视图函数，配置蓝图路由
@view_bule.route("/")
def index():

    bar = pv_day_group()
    bar.render("apps/templates/html/2月PV日流量分析.html")
    return render_template("html/2月PV日流量分析.html")


