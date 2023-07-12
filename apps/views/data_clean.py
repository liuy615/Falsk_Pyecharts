# -*- coding: utf-8 -*
# @Time    : 2023/6/28 11:23
# @Author  : liuy
# @File    : data_clean.py
import pandas as pd
from tools import get_query
from pyecharts.charts import Funnel
from pyecharts import options as opts


# 1. 流量分析
# 1.1 PV/UV流量数据准备
def month_flow_data(read_path, time_start, time_end, save_path):
    # sql1 = 'select user_id,action_time from jdata_action'
    # # 调用函数连接数据库取出数据
    # orginal_data = get_query(sql1)
    # data = pd.DataFrame(orginal_data)
    # print(data)
    data = pd.read_pickle(read_path)
    # pv数据分析
    pv_flow_data = data[(data["action_time"] >= time_start) & (data["action_time"] < time_end)][["user_id", "action_time", "type"]]
    pv_flow_data["day"] = pv_flow_data["action_time"].dt.day
    pv_flow_data["week"] = pv_flow_data["action_time"].dt.day_name()
    pv_flow_data["hour"] = pv_flow_data["action_time"].dt.hour
    pv_day_data = pv_flow_data.groupby("day").agg(num=("user_id", "count")).reset_index()
    pv_week_data = pv_flow_data.groupby("week").agg(num=("user_id", "count")).reset_index()
    pv_hour_data = pv_flow_data.groupby("hour").agg(num=("user_id", "count")).reset_index()
    pv_type_data = pv_flow_data.groupby("type").agg(num=("user_id", "count")).reset_index()
    # uv数据分析
    flow_data = data.drop_duplicates(subset='user_id', keep="first")
    uv_flow_data = flow_data[(flow_data["action_time"] >= time_start) & (flow_data["action_time"] < time_end)][["user_id", "action_time", "type"]]
    uv_flow_data["day"] = uv_flow_data["action_time"].dt.day
    uv_flow_data["week"] = uv_flow_data["action_time"].dt.day_name()
    uv_flow_data["hour"] = uv_flow_data["action_time"].dt.hour
    uv_day_data = uv_flow_data.groupby("day").agg(num=("user_id", "count")).reset_index()
    uv_week_data = uv_flow_data.groupby("week").agg(num=("user_id", "count")).reset_index()
    uv_hour_data = uv_flow_data.groupby("hour").agg(num=("user_id", "count")).reset_index()
    uv_type_data = uv_flow_data.groupby("type").agg(num=("user_id", "count")).reset_index()

    with pd.ExcelWriter(save_path) as writer:
        pv_day_data.to_excel(writer, "pv_day_data", index=False)
        pv_week_data.to_excel(writer, "pv_week_data", index=False)
        pv_hour_data.to_excel(writer, "pv_hour_data", index=False)
        pv_type_data.to_excel(writer, "pv_type_data", index=False)
        uv_day_data.to_excel(writer, "uv_day_data", index=False)
        uv_week_data.to_excel(writer, "uv_week_data", index=False)
        uv_hour_data.to_excel(writer, "uv_hour_data", index=False)
        uv_type_data.to_excel(writer, "uv_type_data", index=False)


# 2. 用户相关分析
def month_user_data(read_path, time_start, time_end, save_path):
    data = pd.read_pickle(read_path)
    data = data[(data["action_time"] >= time_start) & (data["action_time"] < time_end)]
    data["day"] = data["action_time"].dt.day
    data["week"] = data["action_time"].dt.day_name()
    data["hour"] = data["action_time"].dt.hour
    user_data = data.groupby("user_id")
    # 2.1 用户购买量与消费金额分析
    user_buy_money = user_data.agg(F=("sku_id", "count"), M=("money", "sum"), 最近购买时间=("action_time", "max")).sort_values("M", ascending=False).reset_index()
    day_max = data["action_time"].max()
    user_buy_money["R"] = (day_max - user_buy_money["最近购买时间"]).dt.days
    # 2.2 用户累积消费金额占比分析
    user_buy_money["累积金额"] = user_buy_money["M"].cumsum()

    # 2.3 用户消费时间分析
    user_buy_time1 = user_data["day"].agg(lambda x: x.mode().values[0])
    user_buy_time2 = user_data["week"].agg(lambda x: x.mode().values[0])
    user_buy_time3 = user_data["hour"].agg(lambda x: x.mode().values[0])

    user_buy_time = pd.concat([user_buy_time1, user_buy_time2, user_buy_time3], axis=1)
    user_portrait_data = pd.merge(user_buy_money, user_buy_time, how="left", on="user_id")
    print(user_portrait_data)
    # 2.4 用户
    with pd.ExcelWriter(save_path) as writer:
        user_portrait_data.to_excel(writer, "user_portrait_data", index=False)



def main():
    # month_flow_data("../static/data/data_action.pkl", "2018-03-01", "2018-04-01", "../static/3月数据/month_flow_data.xlsx")
    month_user_data("../static/data/data_consumption.pkl", "2018-03-01", "2018-04-01", "../static/3月数据/month_user_data.xlsx")


if __name__ == '__main__':
    main()
    print("程序结束！")
