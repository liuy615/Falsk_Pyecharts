# -*- coding: utf-8 -*
# @Time    : 2023/6/28 11:23
# @Author  : liuy
# @File    : data_clean.py
import pandas as pd
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_columns', 100)


# 1. 流量分析
class MonthFlowData:
    def __init__(self, read_path):
        self.data = pd.read_pickle(read_path)

    # 1.1 PV流量数据准备
    def pv_data(self, time_start, time_end, save_path):
        # pv数据分析
        pv_flow_data = self.data[(self.data["action_time"] >= time_start) & (self.data["action_time"] < time_end)][["user_id", "action_time", "type"]]
        pv_flow_data["day"] = pv_flow_data["action_time"].dt.day
        pv_flow_data["week"] = pv_flow_data["action_time"].dt.day_name()
        pv_flow_data["hour"] = pv_flow_data["action_time"].dt.hour
        pv_day_data = pv_flow_data.groupby("day").agg(num=("user_id", "count")).reset_index()
        pv_week_data = pv_flow_data.groupby("week").agg(num=("user_id", "count")).reset_index()
        pv_hour_data = pv_flow_data.groupby("hour").agg(num=("user_id", "count")).reset_index()
        pv_type_data = pv_flow_data.groupby("type").agg(num=("user_id", "count")).reset_index()
        with pd.ExcelWriter(save_path) as writer:
            pv_day_data.to_excel(writer, "pv_day_data", index=False)
            pv_week_data.to_excel(writer, "pv_week_data", index=False)
            pv_hour_data.to_excel(writer, "pv_hour_data", index=False)
            pv_type_data.to_excel(writer, "pv_type_data", index=False)

    # 1.2 UV流量数据准备
    def uv_data(self, time_start, time_end, save_path):
        flow_data = self.data.drop_duplicates(subset='user_id', keep="first")
        uv_flow_data = flow_data[(flow_data["action_time"] >= time_start) & (flow_data["action_time"] < time_end)][["user_id", "action_time", "type"]]
        uv_flow_data["day"] = uv_flow_data["action_time"].dt.day
        uv_flow_data["week"] = uv_flow_data["action_time"].dt.day_name()
        uv_flow_data["hour"] = uv_flow_data["action_time"].dt.hour
        uv_day_data = uv_flow_data.groupby("day").agg(num=("user_id", "count")).reset_index()
        uv_week_data = uv_flow_data.groupby("week").agg(num=("user_id", "count")).reset_index()
        uv_hour_data = uv_flow_data.groupby("hour").agg(num=("user_id", "count")).reset_index()
        uv_type_data = uv_flow_data.groupby("type").agg(num=("user_id", "count")).reset_index()
        with pd.ExcelWriter(save_path) as writer:
            uv_day_data.to_excel(writer, "uv_day_data", index=False)
            uv_week_data.to_excel(writer, "uv_week_data", index=False)
            uv_hour_data.to_excel(writer, "uv_hour_data", index=False)
            uv_type_data.to_excel(writer, "uv_type_data", index=False)


class MonthUserData:
    def __init__(self, read_path):
        self.data = pd.read_pickle(read_path)

    # 2. 用户相关分析
    def user_portrait_data(self, time_start, time_end, save_path):
        data = self.data[(self.data["action_time"] >= time_start) & (self.data["action_time"] < time_end)].copy()
        data["day"] = data["action_time"].dt.day
        data["week"] = data["action_time"].dt.day_name()
        data["hour"] = data["action_time"].dt.hour
        user_data = data.groupby("user_id")
        # 2.1 用户购买量与消费金额分析
        user_buy_money = user_data.agg(F=("sku_id", "count"), M=("money", "sum"), last_purchase_time=("action_time", "max")).sort_values("M", ascending=False).reset_index()
        day_max = data["action_time"].max()
        user_buy_money["R"] = (day_max - user_buy_money["last_purchase_time"]).dt.days
        # 2.2 用户累积消费金额占比分析
        user_buy_money["cum_money"] = user_buy_money["M"].cumsum()

        # 2.3 用户消费时间分析
        user_buy_time1 = user_data["day"].agg(lambda x: x.mode().values[0])
        user_buy_time2 = user_data["week"].agg(lambda x: x.mode().values[0])
        user_buy_time3 = user_data["hour"].agg(lambda x: x.mode().values[0])
        user_buy_time = pd.concat([user_buy_time1, user_buy_time2, user_buy_time3], axis=1)

        # 2.6 用户特征数据合并保存
        user_face_data = pd.merge(user_buy_money, user_buy_time, how="left", on="user_id")
        user_base_info = pd.read_csv("../static/data/data_user.csv", index_col=0)
        user_base_info["age"] = user_base_info["age"].astype(int)
        user_base_info["sex"] = user_base_info["sex"].astype(int)
        user_base_info["user_lv_cd"] = user_base_info["user_lv_cd"].astype(int)
        user_base_info["city_level"] = user_base_info["city_level"].astype(int)
        user_base_info["province"] = user_base_info["province"].astype(int)
        user_base_info["city"] = user_base_info["city"].astype(int)
        user_base_info["county"] = user_base_info["county"].astype(int)
        user_face_data = pd.merge(user_face_data, user_base_info, how="left", on="user_id")

        print(user_face_data)
        user_face_data.to_csv(save_path, encoding="utf-8")


def main():
    # 2月数据准备
    # month_flow_data = MonthFlowData("../static/data/data_action.pkl")
    # month_flow_data.pv_data("2018-02-01", "2018-03-01", "../static/2月数据/month_pv_data.xlsx")
    # month_flow_data.uv_data("2018-02-01", "2018-03-01", "../static/2月数据/month_uv_data.xlsx")
    # 3月数据准备
    # month_flow_data = MonthFlowData("../static/data/data_action.pkl")
    # month_flow_data.pv_data("2018-03-01", "2018-04-01", "../static/3月数据/month_pv_data.xlsx")
    # month_flow_data.uv_data("2018-03-01", "2018-04-01", "../static/3月数据/month_uv_data.xlsx")
    month_user_data = MonthUserData("../static/data/data_consumption.pkl")
    month_user_data.user_portrait_data("2018-03-01", "2018-04-01", "../static/3月数据/user_portrait_data.csv")


if __name__ == '__main__':
    main()
    print("程序结束！")
