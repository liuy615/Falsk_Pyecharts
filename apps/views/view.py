# -*- coding: utf-8 -*
# @Time    : 2023/6/25 14:11
# @Author  : liuy
# @File    : view.py
import numpy as np
import pandas as pd
from flask import render_template, Blueprint, jsonify
from apps.views.draw import MonthFlow


view_bule = Blueprint("view", __name__)


# 1. echarts日报可视化大屏主页
now_day = "2018-03-02"
now_day_flow_path = f"apps/static/日报数据/日报{now_day}日数据.xlsx"


@view_bule.route("/")
def index():
    data_member = pd.read_excel(now_day_flow_path, sheet_name="user_member_data", index_col=0)
    data_flow = pd.read_excel(now_day_flow_path, sheet_name="now_day_flow", index_col=0)
    data_shop_cate = pd.read_excel(now_day_flow_path, sheet_name="sale_data_cate", index_col=0)
    data_shop_shop = pd.read_excel(now_day_flow_path, sheet_name="sale_data_shop", index_col=0)
    data_shop_sku = pd.read_excel(now_day_flow_path, sheet_name="sale_data_sku", index_col=0)
    data = {
        "user_member": {
            "member_sum": data_member.loc["num", "member_sum"],
            "member_rate": data_member.loc["num", "member_rate"],
            "user_buy_sum": data_member.loc["num", "user_buy_sum"],
            "member_buy_rate": data_member.loc["num", "member_buy_rate"],
        },
        "data_flow": {
            "pv": data_flow.loc["PV", now_day],
            "pv_YOY": data_flow.loc["PV", "YOY"],
            "pv_QOQ": data_flow.loc["PV", "QOQ"],
            "uv": data_flow.loc["UV", now_day],
            "uv_YOY": data_flow.loc["UV", "YOY"],
            "uv_QOQ": data_flow.loc["UV", "QOQ"],
            },
        "l2": {

        },
        "data_shop": {
            "cate": data_shop_cate.index[0],
            "shop": data_shop_shop.index[0],
            "sku": data_shop_sku.index[0],
        }}
    print(f"index页面数据:{data}\n")
    return render_template("index.html", **data)


# 以下是中间靠左边的可视化图表所需数据
@view_bule.route("/l2")
def echarts_l2():
    user_member_data = pd.read_excel(now_day_flow_path, sheet_name="user_member_data", index_col=0)
    member_sex_data = pd.read_excel(now_day_flow_path, sheet_name="member_sex", index_col=0)
    data = {"user_sum": int(user_member_data.loc["num", "user_sum"] - user_member_data.loc["num", "member_sum"]), "member_sum": int(user_member_data.loc["num", "member_sum"]),
            "man": int(member_sex_data.loc[0, "sex"]), "woman": int(member_sex_data.loc[1, "sex"]), "未知": int(member_sex_data.loc[-1, "sex"])}
    print(f"l2图表数据：{data}\n")
    return jsonify(data)


@view_bule.route("/l3")
def echarts_l3():
    user_member_data = pd.read_excel(now_day_flow_path, sheet_name="user_member_data", index_col=0)
    member_age_data = pd.read_excel(now_day_flow_path, sheet_name="member_age", index_col=0)
    data = {"user_sum": int(user_member_data.loc["num", "user_sum"] - user_member_data.loc["num", "member_sum"]), "member_sum": int(user_member_data.loc["num", "member_sum"]),
            "15以下": int(member_age_data.loc[1, "age"]), "15-25": int(member_age_data.loc[2, "age"]), "25-35": int(member_age_data.loc[3, "age"]),
            "35-45": int(member_age_data.loc[4, "age"]), "45-55": int(member_age_data.loc[5, "age"]), "55以上": int(member_age_data.loc[6, "age"])}
    print(f"l2图表数据：{data}\n")
    return jsonify(data)


@view_bule.route("/l4")
def echarts_l4():
    user_member_data = pd.read_excel(now_day_flow_path, sheet_name="user_member_data", index_col=0)
    member_lv_cd_data = pd.read_excel(now_day_flow_path, sheet_name="member_lv_cd", index_col=0)
    data = {"user_sum": int(user_member_data.loc["num", "user_sum"] - user_member_data.loc["num", "member_sum"]), "member_sum": int(user_member_data.loc["num", "member_sum"]),
            "member_lv_index": member_lv_cd_data.index.tolist(), "member_lv_data": member_lv_cd_data["user_lv_cd"].tolist()}
    print(f"l2图表数据：{data}\n")
    return jsonify(data)


# 以下是中间靠左边的可视化图表所需数据
@view_bule.route("/lc2")
def echarts_lc2():
    data_flow = pd.read_excel(now_day_flow_path, sheet_name="now_day_flow", index_col=0)
    data = {"lc2_index": ['2018-02-02', '2018-03-01', '2018-03-02'],  # 这里的index可以获取当前的日期，然后对日期取数
            "lc2_pv": data_flow.iloc[0, 0:3].tolist(),
            "lc2_uv": data_flow.iloc[1, 0:3].tolist()}
    print(f"lc2图表数据：{data}\n")
    return jsonify(data)


@view_bule.route("/lc3")
def echarts_lc3():
    data_action = pd.read_excel(now_day_flow_path, sheet_name="now_day_action", index_col=0)
    data = {"browse_add": int(data_action.iloc[0, 0]), "browse_save": int(data_action.iloc[0, 1]), "browse_buy": int(data_action.iloc[0, 2]),
            "add_save": int(data_action.iloc[0, 4]), "add_buy": int(data_action.iloc[0, 5]), "save_buy": int(data_action.iloc[0, 8])}
    print(f"lc3图表数据：{data}\n")
    return jsonify(data)


@view_bule.route("/lc4")
def echarts_lc4():
    data_active = pd.read_excel(now_day_flow_path, sheet_name="now_day_active", index_col=0)
    data = {"lc4_index": data_active.index.tolist(),
            "lc4_pv": data_active["pv_active_time"].tolist(),
            "lc4_uv": data_active["uv_active_time"].tolist()}
    print(f"lc4图表数据：{data}\n")
    return jsonify(data)


# 以下是中间靠右边的可视化图表所需数据
@view_bule.route("/cr3")
def echarts_cr3():
    data_csv = pd.read_csv("apps/static/data/data_user.csv")
    data_csv["year"] = pd.to_datetime(data_csv["user_reg_tm"]).dt.year
    data_reg_time = data_csv["year"].value_counts(sort=False).sort_index()
    data = {"日期": data_reg_time.index.tolist(), "num": data_reg_time.tolist()}
    print(f"cr3图表数据：{data}\n")
    return jsonify(data)


# 以下是最右边的可视化图表所需数据
@view_bule.route("/r2")
def echarts_r2():
    data_cate = pd.read_excel(now_day_flow_path, sheet_name="data_cate", index_col=0)
    r2_index, r2_index_top3 = data_cate.index.tolist(), data_cate[0:3].index.tolist()
    r2_cate, r2_cate_top3 = data_cate["cate"].tolist(), data_cate["cate"][0:3].tolist()
    r2_data, r2_data_top3 = dict(zip(r2_index, r2_cate)), dict(zip(r2_index_top3, r2_cate_top3))
    sale_data_cate = pd.read_excel(now_day_flow_path, sheet_name="sale_data_cate", index_col=0)
    r2_sale_index, r2_sale_index_top3 = sale_data_cate.index.tolist(), sale_data_cate[0:3].index.tolist()
    r2_sale_cate, r2_sale_cate_top3 = sale_data_cate["cate"].tolist(), sale_data_cate["cate"][0:3].tolist()
    r2_sale_data, r2_sale_data_top3 = dict(zip(r2_sale_index, r2_sale_cate)), dict(zip(r2_sale_index_top3, r2_sale_cate_top3))
    data = {"cate": r2_data, "sale_cate": r2_sale_data, "cate_top3": r2_data_top3, "sale_cate_top3": r2_sale_data_top3}
    print(f"r2图表数据：{data}\n")
    return jsonify(data)


# echarts右2可视化图示数据
@view_bule.route("/r3")
def echarts_r3():
    data_shop = pd.read_excel(now_day_flow_path, sheet_name="data_shop", index_col=0)
    r2_index, r2_index_top3 = data_shop.index.tolist(), data_shop[0:3].index.tolist()
    r2_shop, r2_shop_top3 = data_shop["shop_id"].tolist(), data_shop["shop_id"][0:3].tolist()
    r2_data, r2_data_top3 = dict(zip(r2_index, r2_shop)), dict(zip(r2_index_top3, r2_shop_top3))
    sale_data_shop = pd.read_excel(now_day_flow_path, sheet_name="sale_data_shop", index_col=0)
    r2_sale_index, r2_sale_index_top3 = sale_data_shop.index.tolist(), sale_data_shop[0:3].index.tolist()
    r2_sale_shop, r2_sale_shop_top3 = sale_data_shop["shop_id"].tolist(), sale_data_shop["shop_id"][0:3].tolist()
    r2_sale_data, r2_sale_data_top3 = dict(zip(r2_sale_index, r2_sale_shop)), dict(zip(r2_sale_index_top3, r2_sale_shop_top3))
    data = {"cate": r2_data, "sale_cate": r2_sale_data, "cate_top3": r2_data_top3, "sale_cate_top3": r2_sale_data_top3}
    print(f"r2图表数据：{data}\n")
    return jsonify(data)


# 2. 可视化大屏月报
@view_bule.route("/month_flow")
def month_flow_index():

    return render_template("index-month.html")


last_month, month = 2, 3
last_month_flow_path = f'apps/static/{last_month}月数据/{last_month}月flow数据.xlsx'
month_flow_path = f'apps/static/{month}月数据/{month}月flow数据.xlsx'


# 2.1 月报-pv-流量分析（日）数据准备、传输
@view_bule.route("/month_flow_l1")
def month_flow_echarts_l1():
    last_month_pv_data = pd.read_excel(last_month_flow_path, sheet_name="pv_day_flow", index_col=0)  # 上月的数据
    month_pv_data = pd.read_excel(month_flow_path, sheet_name="pv_day_flow", index_col=0)  # 本月的数据
    pv_day_index = month_pv_data.index.tolist()
    month_pv_data["last_day"] = last_month_pv_data["day"]
    month_pv_data["rate"] = (month_pv_data["day"] - month_pv_data["last_day"])/month_pv_data["last_day"]*100
    month_pv_data["rate"] = round(month_pv_data["rate"], 2)
    month_pv_data = month_pv_data.replace(np.nan, 0)
    pv_day_value = round(month_pv_data["day"]/1000, 2).tolist()
    last_pv_day_value = round(last_month_pv_data["day"]/1000, 2).tolist()
    pv_day_rate = month_pv_data["rate"].tolist()

    data = {"pv_day_index": pv_day_index, "pv_day_value": pv_day_value, "last_pv_day_value": last_pv_day_value, "pv_day_rate": pv_day_rate}
    print(f"month-flow-l1图表数据：{data}\n")
    return jsonify(data)


# 2.2 月报-pv-流量分析(时)数据准备、传输
@view_bule.route("/month_flow_l2")
def month_flow_echarts_l2():
    last_month_pv_data = pd.read_excel(last_month_flow_path, sheet_name="pv_hour_flow", index_col=0)  # 上月的数据
    month_pv_data = pd.read_excel(month_flow_path, sheet_name="pv_hour_flow", index_col=0)  # 本月的数据
    pv_hour_index = month_pv_data.index.tolist()
    month_pv_data["last_hour"] = last_month_pv_data["hour"]
    month_pv_data["rate"] = (month_pv_data["hour"] - month_pv_data["last_hour"])/month_pv_data["last_hour"]*100
    month_pv_data["rate"] = round(month_pv_data["rate"], 2)
    month_pv_data = month_pv_data.replace(np.nan, 0)
    pv_hour_value = round(month_pv_data["hour"]/1000, 2).tolist()
    last_pv_hour_value = round(last_month_pv_data["hour"]/1000, 2).tolist()
    pv_hour_rate = month_pv_data["rate"].tolist()

    data = {"pv_hour_index": pv_hour_index, "pv_hour_value": pv_hour_value, "last_pv_hour_value": last_pv_hour_value, "pv_hour_rate": pv_hour_rate}
    print(f"month-flow-l2图表数据：{data}\n")
    return jsonify(data)


# 2.3 月报-pv-流量分析(周次)数据准备、传输
@view_bule.route("/month_flow_l3")
def month_flow_echarts_l3():
    last_month_pv_data = pd.read_excel(last_month_flow_path, sheet_name="pv_week_flow", index_col=0)  # 上月的数据
    month_pv_data = pd.read_excel(month_flow_path, sheet_name="pv_week_flow", index_col=0)  # 本月的数据
    pv_week_index = month_pv_data.index.tolist()
    month_pv_data["last_week"] = last_month_pv_data["week"]
    month_pv_data["rate"] = (month_pv_data["week"] - month_pv_data["last_week"])/month_pv_data["last_week"]*100
    month_pv_data["rate"] = round(month_pv_data["rate"], 2)
    month_pv_data = month_pv_data.replace(np.nan, 0)
    pv_week_value = round(month_pv_data["week"]/1000, 2).tolist()
    last_pv_week_value = round(last_month_pv_data["week"]/1000, 2).tolist()
    pv_week_rate = month_pv_data["rate"].tolist()

    data = {"pv_week_index": pv_week_index, "pv_week_value": pv_week_value, "last_pv_week_value": last_pv_week_value, "pv_week_rate": pv_week_rate}
    print(f"month-flow-l2图表数据：{data}\n")
    return jsonify(data)


# 2.7 月报-uv-流量分析（日）数据准备、传输
@view_bule.route("/month_flow_r1")
def month_flow_echarts_r1():
    last_month_uv_data = pd.read_excel(last_month_flow_path, sheet_name="uv_day_user", index_col=0)  # 上月的数据
    month_uv_data = pd.read_excel(month_flow_path, sheet_name="uv_day_user", index_col=0)  # 本月的数据
    uv_day_index = month_uv_data.index.tolist()
    month_uv_data["last_day_user"] = last_month_uv_data["day_user"]
    month_uv_data["rate"] = (month_uv_data["day_user"] - month_uv_data["last_day_user"])/month_uv_data["last_day_user"]*100
    month_uv_data["rate"] = round(month_uv_data["rate"], 2)
    month_uv_data = month_uv_data.replace(np.nan, 0)
    uv_day_value = round(month_uv_data["day_user"]/1000, 2).tolist()
    last_uv_day_value = round(last_month_uv_data["day_user"]/1000, 2).tolist()
    uv_day_rate = month_uv_data["rate"].tolist()

    data = {"uv_day_index": uv_day_index, "uv_day_value": uv_day_value, "last_uv_day_value": last_uv_day_value, "uv_day_rate": uv_day_rate}
    print(f"month-flow-r1图表数据：{data}\n")
    return jsonify(data)


# 2.8 月报-uv-流量分析(时)数据准备、传输
@view_bule.route("/month_flow_r2")
def month_flow_echarts_r2():
    last_month_uv_data = pd.read_excel(last_month_flow_path, sheet_name="uv_hour_user", index_col=0)  # 上月的数据
    month_uv_data = pd.read_excel(month_flow_path, sheet_name="uv_hour_user", index_col=0)  # 本月的数据
    uv_hour_index = month_uv_data.index.tolist()
    month_uv_data["last_hour_user"] = last_month_uv_data["hour_user"]
    month_uv_data["rate"] = (month_uv_data["hour_user"] - month_uv_data["last_hour_user"])/month_uv_data["last_hour_user"]*100
    month_uv_data["rate"] = round(month_uv_data["rate"], 2)
    month_uv_data = month_uv_data.replace(np.nan, 0)
    uv_hour_value = round(month_uv_data["hour_user"]/1000, 2).tolist()
    last_uv_hour_value = round(last_month_uv_data["hour_user"]/1000, 2).tolist()
    uv_hour_rate = month_uv_data["rate"].tolist()

    data = {"uv_hour_index": uv_hour_index, "uv_hour_value": uv_hour_value, "last_uv_hour_value": last_uv_hour_value, "uv_hour_rate": uv_hour_rate}
    print(f"month-flow-r2图表数据：{data}\n")
    return jsonify(data)


# 2.9 月报-uv-流量分析(周次)数据准备、传输
@view_bule.route("/month_flow_r3")
def month_flow_echarts_r3():
    last_month_uv_data = pd.read_excel(last_month_flow_path, sheet_name="uv_week_user", index_col=0)  # 上月的数据
    month_uv_data = pd.read_excel(month_flow_path, sheet_name="uv_week_user", index_col=0)  # 本月的数据
    uv_week_index = month_uv_data.index.tolist()
    month_uv_data["last_week_user"] = last_month_uv_data["week_user"]
    month_uv_data["rate"] = (month_uv_data["week_user"] - month_uv_data["last_week_user"])/month_uv_data["last_week_user"]*100
    month_uv_data["rate"] = round(month_uv_data["rate"], 2)
    month_uv_data = month_uv_data.replace(np.nan, 0)
    uv_week_value = round(month_uv_data["week_user"]/1000, 2).tolist()
    last_uv_week_value = round(last_month_uv_data["week_user"]/1000, 2).tolist()
    uv_week_rate = month_uv_data["rate"].tolist()

    data = {"uv_week_index": uv_week_index, "uv_week_value": uv_week_value, "last_uv_week_value": last_uv_week_value, "uv_week_rate": uv_week_rate}
    print(f"month-flow-r2图表数据：{data}\n")
    return jsonify(data)












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