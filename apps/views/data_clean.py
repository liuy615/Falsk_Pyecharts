# -*- coding: utf-8 -*
# @Time    : 2023/6/28 11:23
# @Author  : liuy
# @File    : data_clean.py
import pandas as pd
from tools import get_query


# 1. 流量分析
# 1.1.1 PV流量数据准备
def month_pv_data(read_path, time_start, time_end, save_path):
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
    # uv数据分析
    flow_data = data.drop_duplicates(subset='user_id', keep="first")
    uv_flow_data = flow_data[(flow_data["action_time"] >= time_start) & (flow_data["action_time"] < time_end)][["user_id", "action_time", "type"]]
    uv_flow_data["day"] = uv_flow_data["action_time"].dt.day
    uv_flow_data["week"] = uv_flow_data["action_time"].dt.day_name()
    uv_flow_data["hour"] = uv_flow_data["action_time"].dt.hour
    uv_day_data = uv_flow_data.groupby("day").agg(num=("user_id", "count")).reset_index()
    uv_week_data = uv_flow_data.groupby("week").agg(num=("user_id", "count")).reset_index()
    uv_hour_data = uv_flow_data.groupby("hour").agg(num=("user_id", "count")).reset_index()

    with pd.ExcelWriter(save_path) as writer:
        pv_day_data.to_excel(writer, "pv_day_data", index=False)
        pv_week_data.to_excel(writer, "pv_week_data", index=False)
        pv_hour_data.to_excel(writer, "pv_hour_data", index=False)
        uv_day_data.to_excel(writer, "uv_day_data", index=False)
        uv_week_data.to_excel(writer, "uv_week_data", index=False)
        uv_hour_data.to_excel(writer, "uv_hour_data", index=False)


# 1.1.2

month_pv_data("../static/data/data_action.pkl", "2018-03-01", "2018-04-01", "../static/3月数据/month_flow_data.xlsx")


if __name__ == '__main__':
    print("程序结束！")
