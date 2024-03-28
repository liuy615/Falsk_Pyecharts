# -*- coding: utf-8 -*
# @Time    : 2023/6/28 11:23
# @Author  : liuy
# @File    : data_clean.py
import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from tools import get_query, get_one_query, calculate_time, new_users_vip, get_vip_user
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_columns', 100)


# 1. 日报所需数据
class DayFlowData:
    def __init__(self):
        pass

    # 1.1.1 会员城市分布
    # 1.1.2 会员性别分布
    # 1.1.1 会员等级分布

    def get_user_member(self, now_day):
        sart_time = datetime.datetime.now()
        sql_user_member_action_data = f"select user_id, type from jdata_action where date(action_time)='{now_day}';"
        sql_user_member_user_data = f"select user_id, age, sex, user_lv_cd, city_level, user_reg_tm from jdata_user;"
        user_member_action_data = pd.DataFrame(get_query(sql_user_member_action_data)).drop_duplicates(subset="user_id", keep="first")
        user_member_user_data = pd.DataFrame(get_query(sql_user_member_user_data))
        user_member_data = pd.merge(user_member_action_data, user_member_user_data, on="user_id", how="left")
        # 今日访问用户总数、访问用户中会员数、会员占比、今日下单用户总数、下单用户中会员所占比例
        user_num = user_member_data.shape[0]  # 今日访问用户总数
        member_num = user_member_data.dropna().shape[0]  # 访问用户中会员数
        member_rate = round(member_num/user_num, 4)*100  # 访问用户中会员占比
        user_buy_num = user_member_data[user_member_data["type"] == 4].shape[0]   # 今日下单用户总数
        member_buy_num = user_member_data[user_member_data["type"] == 4].dropna().shape[0]  # 下单用户中会员数
        member_buy_rate = round(member_buy_num/user_buy_num, 4)*100
        result = {"user_sum": user_num, "member_sum": member_num, "member_rate": member_rate,
                  "user_buy_sum": user_buy_num, "member_buy_sum": member_buy_num, "member_buy_rate": member_buy_rate}
        result = pd.DataFrame(result, index=["num"])

        # 会员城市、等级、性别分布
        member_age = user_member_data["age"].value_counts()
        member_sex = user_member_data["sex"].value_counts()
        member_lv_cd = user_member_data["user_lv_cd"].value_counts()
        end_time = datetime.datetime.now()
        print(result, f'总用时{end_time - sart_time}')
        return result, member_age, member_sex, member_lv_cd

    # 1.2.1 每日PV、UV流量数据准备
    def get_user_day_flow(self, now_day):
        """
        此函数用于获取当前日期流量数据，包括pv、uv以及当前日期同比和环比的增长率。
        :return: 当前日期的pv、uv数据，和同比环比数据
        """
        time_now_day = datetime.datetime.strptime(now_day, "%Y-%m-%d")
        last_day = str((time_now_day + relativedelta(days=-1)).strftime("%Y-%m-%d"))
        last_month = str((time_now_day + relativedelta(months=-1)).strftime("%Y-%m-%d"))
        day_time = (now_day, last_day, last_month)
        sql_pv_flow_data = f"select user_id, date(action_time) as action_time, type from jdata_action where date(action_time) in {day_time};"
        data = pd.DataFrame(get_query(sql_pv_flow_data))
        data_group = data.groupby("action_time").agg(PV=("user_id", "count"), UV=("user_id", pd.Series.nunique))
        data_flow = pd.DataFrame(data_group.values.T, columns=[last_month, last_day, now_day], index=data_group.columns)
        data_flow["YOY"] = round((data_flow[now_day] - data_flow[last_month]) / data_flow[last_month], 4)*100
        data_flow["QOQ"] = round((data_flow[now_day] - data_flow[last_day]) / data_flow[last_day], 4)*100
        print(data_flow)
        return data_flow

    # 1.2.2 用户行为路径数据准备
    def get_user_action_way(self, now_day):
        """
        此函数用于获取用户的行为数据，用户的5种行为，浏览、加购、收藏、下单、评论。我们将一个用户浏览一个商品做为一次行为。那么每个用户对
        每一个商品将会产生1-5种不同的行为，我们用一个列表记录下每一个用户的行为路径。
        :return: 返回一个列表，包括用户的所有行为。例如[1,1,0,0,0]:表示用户浏览了一个商品，并且下单。
        """
        sql_user_action_way = f"select user_id, sku_id, type from jdata_action where date(action_time) ='{now_day}';"
        data = pd.DataFrame(get_query(sql_user_action_way))
        data_1 = data[data["type"] == 1]
        data_2 = data[data["type"] == 2]
        data_3 = data[data["type"] == 3]
        data_4 = data[data["type"] == 4]
        data_5 = data[data["type"] == 5]
        print(data_1.shape, data_2.shape, data_3.shape, data_4.shape, data_5.shape)

        def get_data(user, sku, data_type):
            if user in data_type["user_id"].values:
                data_df = data_type[data_type["user_id"] == user]
                if sku in data_df["sku_id"].values:
                    list_row.append(1)
                else:
                    list_row.append(0)
            else:
                list_row.append(0)

        type_data = []
        for key, value in data_1.iterrows():
            list_row = [1, ]
            user_id = value["user_id"]
            sku_id = value["sku_id"]
            get_data(user_id, sku_id, data_2)
            get_data(user_id, sku_id, data_3)
            get_data(user_id, sku_id, data_4)
            get_data(user_id, sku_id, data_5)
            type_data.append(list_row)

        data_type = pd.DataFrame(type_data, columns=["1", "2", "3", "4", "5"])
        browse_add = data_type[(data_type["2"] == 1) & (data_type["3"] == 0) & (data_type["4"] == 0)].shape[0]  # 浏览-加购人数
        browse_save = data_type[(data_type["2"] == 0) & (data_type["3"] == 1) & (data_type["4"] == 0)].shape[0]  # 浏览-收藏人数
        browse_buy = data_type[(data_type["2"] == 0) & (data_type["3"] == 0) & (data_type["4"] == 1)].shape[0]  # 浏览-直接购买人数
        browse_leave = data_type[(data_type["2"] == 0) & (data_type["3"] == 0) & (data_type["4"] == 0)].shape[0]  # 浏览-离开人数
        add_save = data_type[(data_type["2"] == 1) & (data_type["3"] == 1) & (data_type["4"] == 0)].shape[0]  # 加购-收藏人数
        add_buy = data_type[(data_type["2"] == 1) & (data_type["3"] == 0) & (data_type["4"] == 1)].shape[0]  # 加购-直接下单人数
        add_save_buy = data_type[(data_type["2"] == 1) & (data_type["3"] == 1) & (data_type["4"] == 1)].shape[0]  # 加购-收藏-下单人数
        add_leave = data_type[(data_type["2"] == 1) & (data_type["3"] == 0) & (data_type["4"] == 0)].shape[0]  # 加购-离开人数
        save_buy = data_type[(data_type["2"] == 0) & (data_type["3"] == 1) & (data_type["4"] == 1)].shape[0]  # 收藏-下单人数
        save_leave = data_type[(data_type["2"] == 0) & (data_type["3"] == 1) & (data_type["4"] == 0)].shape[0]  # 收藏-离开人数
        buy_comment = data_type[(data_type["4"] == 1) & (data_type["5"] == 1)].shape[0]  # 下单-评论人数
        dic_data = {"browse_add": browse_add, "browse_save": browse_save, "browse_buy": browse_buy, "browse_leave": browse_leave,
                    "add_save": add_save, "add_buy": add_buy, "add_save_buy": add_save_buy, "add_leave": add_leave,
                    "save_buy": save_buy, "save_leave": save_leave, "buy_comment": buy_comment,
                    }
        dic_data = pd.DataFrame(dic_data, index=["num"])
        print(dic_data)
        return dic_data

    # 1.2.3 用户活跃时间数据准备
    def get_user_active_time(self, now_day):
        sql_user_active_time = f"select user_id, hour(action_time) as action_hour from jdata_action where date(action_time) ='{now_day}';"
        pv_data = pd.DataFrame(get_query(sql_user_active_time))
        pv_active_time = pv_data.value_counts("action_hour", sort=False)
        uv_data = pv_data.groupby("user_id").agg(lambda x: pd.Series.mode(x)[0]).reset_index()
        uv_active_time = uv_data.value_counts("action_hour", sort=False).astype(str)
        active_time = pd.DataFrame({"pv_active_time": pv_active_time, "uv_active_time": uv_active_time}, index=pv_active_time.index.values)
        print(active_time)
        return active_time

    # 1.4.1 商品数据：今日浏览量前三的品类/销量前三的品类
    # 1.4.2 商品数据：今日浏览量前三的单品/销量前三的单品
    # 1.4.3 商品数据：今日浏览量前三的店铺/销量前三的店铺
    def get_product_cate(self, now_day):
        sql_product_cate = f"select action.sku_id, type, shop_id, cate from jdata_action as action inner join jdata_product as product on action.sku_id = product.sku_id where date(action_time)='{now_day}';"
        data = pd.DataFrame(get_query(sql_product_cate))
        data_sku = data["sku_id"].value_counts()[:10]
        data_shop = data["shop_id"].value_counts()[:10]
        data_cate = data["cate"].value_counts()[:10]
        print(f"浏览量前三的单品\n{data_sku}\n 浏览量前三的店铺\n{data_shop}\n 浏览量前三的品类\n{data_cate}")
        sale_data = data[data["type"] == 4]
        sale_data_sku = sale_data["sku_id"].value_counts()[:10]
        sale_data_shop = sale_data["shop_id"].value_counts()[:10]
        sale_data_cate = sale_data["cate"].value_counts()[:10]
        print(f"销量前三的单品\n{sale_data_sku}\n 销量前三的店铺\n{sale_data_shop}\n 销量前三的品类\n{sale_data_cate}")
        return data_sku, data_shop, data_cate, sale_data_sku, sale_data_shop, sale_data_cate

    # 1.5 将当日相关数据进行保存
    def save_data(self, now_day):
        data_flow = self.get_user_day_flow(now_day)
        data_action_way = self.get_user_action_way(now_day)
        data_active_time = self.get_user_active_time(now_day)
        data_sku, data_shop, data_cate, sale_data_sku, sale_data_shop, sale_data_cate = self.get_product_cate(now_day)
        result, member_age, member_sex, member_lv_cd = self.get_user_member(now_day)
        with pd.ExcelWriter("../static/日报数据/日报{}日数据.xlsx".format(now_day)) as writer:
            data_flow.to_excel(writer, "now_day_flow", index=True)
            data_action_way.to_excel(writer, "now_day_action", index=True)
            data_active_time.to_excel(writer, "now_day_active", index=True)
            data_sku.to_excel(writer, "data_sku", index=True)
            data_shop.to_excel(writer, "data_shop", index=True)
            data_cate.to_excel(writer, "data_cate", index=True)
            sale_data_sku.to_excel(writer, "sale_data_sku", index=True)
            sale_data_shop.to_excel(writer, "sale_data_shop", index=True)
            sale_data_cate.to_excel(writer, "sale_data_cate", index=True)
            result.to_excel(writer, "user_member_data", index=True)
            member_age.to_excel(writer, "member_age", index=True)
            member_sex.to_excel(writer, "member_sex", index=True)
            member_lv_cd.to_excel(writer, "member_lv_cd", index=True)


# 2. 按月流量分析
class MonthFlow:
    def __init__(self):
        pass

    @calculate_time
    def read_month_action_data(self, year, month):
        query = f'select user_id, type, day(action_time)  day, hour(action_time) hour, weekday(action_time) week from jdata_action where (year(action_time) = {year}) and (month(action_time) = {month});'
        get_one_query(query, f"../static/{month}月数据/{month}月flow原始数据.csv")

    def type_conversion(self, month):
        """
        将读取的数据进行数据类型精确，并返回dataframe
        """
        month_action_data = pd.read_csv(f"../static/{month}月数据/{month}月flow原始数据.csv", chunksize=5000000)
        flow_data = pd.DataFrame()
        for chunk in month_action_data:
            chunk["user_id"] = chunk["user_id"].astype(np.int16)
            chunk[["hour", "day", "type"]] = chunk[["hour", "day", "type"]].astype(np.int8)
            flow_data = flow_data.append(chunk)
        return flow_data
    """
    2.1 流量对比分析PV、UV、人均浏览量（访问广度）（对比分析: 与行业平均值对比，同比、环比，与公司历史平均值对比）
        1. 日流量与上月进行对比
        2. 周一至周日流量变化（但是需要做平均化处理，避免一个月中某几天多余其他天数）
        3. 0-23时流量变化，与上月进行对比
        4. 人均浏览量（PV/UV）
    """
    def user_flow_analysis(self, month):
        flow_data = self.type_conversion(month)
        # pv计算
        pv_day_flow = flow_data["day"].value_counts().sort_index()   # 获取到pv的日流量分布
        pv_hour_flow = flow_data["hour"].value_counts().sort_index()    # 获取到pv的时流量分布
        pv_week_flow = flow_data.groupby("week").agg(weeks=("user_id", "count")).reset_index()   # 获取到pv的时流量分布
        day_week = flow_data.drop_duplicates(subset="day", keep="first")["week"].value_counts().reset_index()  # 获取这个月有几个星期一
        pv_week_flow = pd.merge(pv_week_flow, day_week, how="inner", left_on="week", right_on="index").set_index("week_x")
        pv_week_flow["week"] = round(pv_week_flow["weeks"]/pv_week_flow["week_y"]).astype(int)
        pv_week_flow = pv_week_flow["week"]
        print(pv_day_flow, pv_hour_flow, pv_week_flow)

        # uv计算：在一个时间周期内，访问页面的人数之和
        uv_day_user = flow_data.groupby("day").agg(day_user=("user_id", "nunique"))
        uv_hour_user = flow_data.groupby("hour").agg(hour_user=("user_id", "nunique"))
        uv_week_user = flow_data.groupby("week").agg(week_users=("user_id", "nunique")).reset_index()
        uv_week_user = pd.merge(uv_week_user, day_week, how="inner", left_on="week", right_on="index").set_index("week_x")
        uv_week_user["week_user"] = round(uv_week_user["week_users"]/uv_week_user["week_y"]).astype(int)
        uv_week_user = uv_week_user["week_user"]
        print(uv_day_user, uv_hour_user, uv_week_user)

        with pd.ExcelWriter(f"../static/{month}月数据/{month}月flow数据.xlsx") as writer:
            pv_day_flow.to_excel(writer, "pv_day_flow")
            pv_hour_flow.to_excel(writer, "pv_hour_flow")
            pv_week_flow.to_excel(writer, "pv_week_flow")
            uv_day_user.to_excel(writer, "uv_day_user")
            uv_hour_user.to_excel(writer, "uv_hour_user")
            uv_week_user.to_excel(writer, "uv_week_user")

    """
    2.2 流量渠道来源分析
        1. 流量渠道来源面积图（可以直观看出哪个渠道贡献率最高）
        2. 流量渠道来源较上月对比柱状图（可以直观看出各渠道是否增加预算）
        3. 流量渠道质量/转化率（投入成本/曝光量/留存率/活跃率）
    """
    """
    2.3 新增用户分析
        1. 新增用户/会员（日）较上月对比柱状图
        2. 
    """
    """
    2.4 用户活跃率分析
        1. 日活
        2. 用户分类的定义:
            1. 新增用户：将不在jdata_user表中的用户定义为新增用户
            2. 活跃用户：在某个周期内有记录的用户定义为活跃用户
            3. 忠诚用户：将连续两周都有活跃的用户定义为忠诚用户
            4. 不活跃用户：将连续两周没有活跃的用户定义为不活跃用户
            5. 流失用户：将两周以上为活跃用户定义为流失用户
            6. 回流用户：至少两周未活跃的用户并重新活跃的用户定义为回流用户
    """
    @calculate_time
    def user_active_analysis(self, month):
        """
        用户活跃率分析, 将会得到每个月中的每一天用户活跃率、新增用户、活跃用户、忠诚用户等，
        :param month: 月份
        :return: dataframe["day", "view_user", "new_user", "old_user", "vip_user", "old_active_rate"]
        """

        def user_active_rate():
            """
            下面计算用户在month月内每天浏览人数，新增用户人数，老用户人数，会员总人数
            新增用户的计算逻辑
                1. 我们得到的数据是2-1至4-15日用户浏览数据，和jdata_user会员表
                2. 我们将会员表中的用户看作老用户，不在表中的用户看作新用户
                3. 新用户在登录过一次之后，自动成为新增老用户，添加到new_user_data表中，以此类推
            此方法返回意义dataframe，包括每日新增用户和老用户
            """
            # 数据提取与数据清洗
            sql_data = f'select distinct user_id, day(action_time) day from jdata_action where year(action_time) ="2018" and month(action_time) = "{month}";'
            data = pd.DataFrame(get_query(sql_data))
            data["user_id"] = data["user_id"].astype(int)
            data["day"] = data["day"].astype(np.int8)
            vip_user_data = get_vip_user()  # 获取jdata_user表中的会用数据
            # 计算用户日活
            day_users_data = pd.DataFrame()
            new_user_data = pd.DataFrame()
            day_user_info = []
            for i in range(1, data["day"].max()+1):
                user_data = pd.merge(data[data["day"] == i], vip_user_data, how="left", on="user_id").fillna(0)
                day_users_data = day_users_data.append(user_data)
                new_users = user_data[user_data["vip"] == 0].loc[:, ["user_id", "vip"]]
                # 然后将新增用户放在new_user_data表中
                new_users["vip"] = 1
                new_users["new"] = 1
                new_user_data = new_user_data.append(new_users)
                # 然后合并user_data和new_user_data，不在new_user_data中的为老用户。

                print(f'第{i}天,浏览人数{user_data.shape[0]},新增会员人数{user_data[user_data["vip"] == 0].shape[0]},老用户人数{user_data[user_data["vip"] == 1].shape[0]},会员人数{vip_user_data.shape[0]}')
                user_dic = {"day": i,
                            "view_user": user_data.shape[0],
                            "new_vip_user": user_data[user_data["vip"] == 0].shape[0],
                            "old_vip_user": user_data[user_data["vip"] == 1].shape[0],
                            "vip_user": vip_user_data.shape[0]
                            }
                day_user_info.append(user_dic)
            day_user_info = pd.DataFrame(day_user_info, columns=["day", "view_user", "new_vip_user", "old_vip_user", "vip_user"])
            day_user_info["old_active_rate"] = round(day_user_info["old_vip_user"] / day_user_info["vip_user"]*100, 2)
            return day_user_info

        def user_active_continue(flow_data):
            """
            计算用户在过去一个月内连续最长登录天数
            :param data: dataframe["user_id", "day"]
            :return: dataframe，["user_id", "day_count", "day_min", "day_max"]
            """
            # 方法二：使用pandas自带的窗口函数,rank
            flow_data.sort_values(by=["user_id", "day"], ascending=[True, True], inplace=True)
            user_data_group = pd.to_datetime(flow_data["day"]) - pd.to_timedelta(flow_data.groupby("user_id")["day"].rank(method="dense", ascending=True), unit='d')
            user_group = flow_data.groupby(by=["user_id", user_data_group], as_index=False).agg(day_continue=("day", "count"), day_min=("day", "min"), day_max=("day", "max"))
            # 筛选各分组中排名第一的一行，如果是第一，则返回ture，否则返回false，配合后面pandas过滤的特性直接筛选出各分组的第一
            mask = user_group.groupby("user_id")["day_continue"].rank(method="first", ascending=False) == 1
            cycle_data = user_group[mask].sort_values(["day_continue", "user_id"], ascending=[False, True])
            print(f"用户连续登录数据计算完成，总共{cycle_data.shape[0]}用户")
            return cycle_data

        def user_active_cycle(flow_data, today):
            """
            计算用户过去5天内登录几天，过去10天内登录几天，过去一个月内登录几天
            用户活跃率分类：
                0. 忠实用户：过去7天内登录天数>=5天
                1. 活跃用户：过去7天内登录天数>=3天
                2. 不活跃用户：过去7天内登录天数0-3天，且过去14天内登录天数>=1天
                3. 流失用户：过去7天内无登录，且过去14天内无登录, 且过去一个月内登录天数<3天
                4. 回流用户：过去7天内登录天数>1天，且过去14天内无登录,且过去两个月内无登录（类似于新增用户，只是回力用户以前登录过）
            :param data: dataframe["user_id", "day"]
            :return: dataframe，["user_id", "day_count", "day_min", "day_max"]
            """
            user_data_7 = flow_data[flow_data["day"] >= (today - pd.to_timedelta(7, unit='d'))]
            user_data_14 = flow_data[flow_data["day"] >= (today - pd.to_timedelta(14, unit='d'))]
            user_data_30 = flow_data[flow_data["day"] >= (today - pd.to_timedelta(30, unit='d'))]
            user_data_7_group = user_data_7.groupby("user_id", as_index=False).agg(day_7=("day", "count"))
            user_data_14_group = user_data_14.groupby("user_id", as_index=False).agg(day_14=("day", "count"))
            user_data_30_group = user_data_30.groupby("user_id", as_index=False).agg(day_30=("day", "count"))
            user_cycle = pd.merge(user_data_30_group, user_data_14_group, on="user_id", how="left")
            user_cycle = pd.merge(user_cycle, user_data_7_group, on="user_id", how="left").fillna(0)
            user_cycle[["day_30", "day_14", "day_7"]] = user_cycle[["day_30", "day_14", "day_7"]].astype(np.int8)
            print(f"用户登录周期数据计算完成，总共{user_cycle.shape[0]}用户")
            return user_cycle

        # 日活（总用户）、新增用户、老用户、老用户活跃率
        user_data_rate = user_active_rate()
        print(user_data_rate)

        # data_list = []
        # # 下面计算用户在过去一个月内连续最长登录天数
        # for today in pd.date_range(pd.to_datetime(f"2018-{month}-" + "1"), pd.to_datetime(f"2018-{month+1}-" + "1") - pd.to_timedelta(1, unit='d')):
        #     sql_data = f"select distinct user_id, date(action_time) day from jdata_action  where date(action_time) between date_sub('{today}',interval 1 month) and '{today}';"
        #     data = pd.DataFrame(get_query(sql_data))
        #     data["user_id"] = data["user_id"].astype(np.int16)
        #     data["day"] = pd.to_datetime(data["day"])
        #     print(f'{today}数据读取完成，总共{data.shape[0]}条用户数据')
        #     user_continue = user_active_continue(data)
        #     user_cycle = user_active_cycle(data, today)
        #     user_data = pd.merge(user_continue, user_cycle, on="user_id", how="left")
        #     loyal_users = user_data[(user_data["day_7"] >= 3) & (user_data["day_14"] >= 7) & (user_data["day_30"] >= 10)]
        #     active_users = user_data[(user_data["day_7"] >= 1) & (user_data["day_14"] >= 3) & (user_data["day_30"] >= 5)]
        #     unactive_users = user_data[(user_data["day_7"] < 1) & (user_data["day_14"] < 3) & (user_data["day_30"] < 5)]
        #     lost_users = user_data[(user_data["day_7"] < 1) & (user_data["day_14"] < 1) & (user_data["day_30"] < 2)]
        #     recurring_users = user_data[(user_data["day_7"] == user_data["day_14"]) & (user_data["day_14"] == user_data["day_30"])]
        #     # 这里需要区分一下新增用户和回流用户：新增用户：本月第一次登录。回流用户：在jdata_user表中存在的用户。
        #     print(f'忠实用户{loyal_users.shape[0]}, 活跃用户{active_users.shape[0]}, 不活跃用户{unactive_users.shape[0]}, 流失用户{lost_users.shape[0]}, 回流用户{recurring_users.shape[0]}, 时间：{datetime.datetime.now()}')
        #     data_dic = {"day": today.day,
        #                 "忠实用户": loyal_users.shape[0],
        #                 "活跃用户": active_users.shape[0],
        #                 "不活跃用户": unactive_users.shape[0],
        #                 "流失用户": lost_users.shape[0],
        #                 "回流用户": recurring_users.shape[0]}
        #     data_list.append(data_dic)
        # user_data_classify = pd.DataFrame(data_list, columns=["day", "忠实用户", "活跃用户", "不活跃用户", "流失用户", "回流用户"])
        # user_active_data = pd.merge(user_data_rate, user_data_classify, on="day", how="left")
        # print(user_active_data)

        # user_active_data.to_excel(f"../static/{month}月数据/{month}月active数据.xlsx", index=False)

    """
    2.5 用户留存率分析
        1. 留存率定义：第n天的留存率 = 第n天留存用户/第n天新增用户
        2. 比如：计算2月1日的次日留存率：（在2-1日登录过平台并且在2-2日也登录了该平台的用户总和）/ 在2-1日新增的用户
                计算2月2日的次日留存率：（在2-2日登录过平台并且在2-3日也登录了该平台的用户总和）/ 在2-2日新增的用户
        3. 留存率分为两类：
            1. 新增留存率： 指的是只看该用户是否是新用户
            2. 活跃留存率： 指的是该用户是老用户，以前登录活平台的用户
            这里由于数据不全，我们只能将不是会员（不在jdata_user表中的用户定义为新增用户，在表中的用户定义为活跃用户/会员用户/老用户）
    """
    def user_retention_analysis(self, month):
        flow_data = self.type_conversion(month).loc[:, ["user_id", "day"]]
        user_data = new_users_vip(flow_data)

        def user_retention_rate(vip):
            now_day_rate = []
            for key in range(1, flow_data["day"].max()):
                rate = []
                new_user = user_data[(user_data["vip"] == vip) & (user_data["day"] == key)]
                i = 1
                while True:
                    if key + i <= user_data["day"].max():
                        new_users = new_user.shape[0]   # 2-1日新增会员总数
                        user_day = pd.merge(user_data[user_data["day"] == key+i], new_user, how="inner", on="user_id").shape[0]  # 在2-1日登录过平台并且在2-2日也登录了该平台的用户总和
                        retained_rate = round(user_day/new_users*100, 2)
                        rate.append(retained_rate)
                        i += 1
                    else:
                        break
                now_day_rate.append(rate)
                print(f'第{key}天留存率：{rate}')
            # 将计算好的留存率转为dataframe然后储存
            day_index = [f'{month}月{key}日' for key in range(1, user_data["day"].max())]
            retain_index = [f'day{key}' for key in range(1, user_data["day"].max())]
            now_day_rate = pd.DataFrame(now_day_rate, index=day_index, columns=retain_index)
            return now_day_rate
        now_day_rate = user_retention_rate(0)
        print(now_day_rate)

    """
    2.6 用户转化率分析
    """
    def user_conversion_rate(self, flow_data):
        pass

    """
    2.7 用户路径分析
    """
    def user_path_analysis(self, flow_data):
        pass

    """
    2.8 用户价值分析（RFM模型）(活跃率分类)
        1. 活跃率分类
            写一个方法：功能：计算今日新增用户，活跃用户，忠诚用户，不活跃用户，流失用户，回流用户
            例如：2-1日，活跃用户：xx， 新增用户：xx， 忠诚用户：0， 不活跃用户：0， 流失用户：0， 回流用户：0
            累计登录天数：
            连续登录天数：
            上次登录时间：
        2. RFM模型 
    """

    def user_value_analysis(self):
        def user_views_data():
            """
            用户保存用户浏览数据
            :return:
            """
            user_data_views = pd.DataFrame()
            for i in range(2, 5):
                data_views = self.type_conversion(i).loc[:, ["user_id", "day"]]
                data_views["day"] = pd.to_datetime(f"2018-{i}-" + data_views["day"].map(str))
                data_views = data_views.drop_duplicates()
                user_data_views = user_data_views.append(data_views)
                print(f'{i}月共{data_views.shape[0]}用户')
            print(user_data_views)
            user_data_views.to_csv("../static/data/user_views_cycle.csv", index=None)
        # user_views_data()

        @calculate_time
        def user_views_cycle():
            user_data = pd.read_csv("../static/data/user_views_cycle.csv")
            user_data["day"] = pd.to_datetime(user_data["day"])
            # user_data = user_data.loc[:1000]    # 测试数据，只有前10000条

            def fun1_cycle():
                """
                方法一：自创方法：
                    1. 先对用户id、日期进行排序
                    2. 计算一列cycle：下一个日期 - 上一个日期 ！= 1，如果=1返回false则说明两个日期是相连的，如果！=1返回true则说明两个日期是断开的
                    3. 计算cycle相同的个数，就是用户在这一段时间连续登录的天数
                """

                user_data.sort_values(by=["user_id", "day"], ascending=[True, True], inplace=True)
                data = []
                for name, group in user_data.groupby("user_id"):
                    group["cycle"] = ((group["day"].diff().fillna(pd.to_timedelta(1, unit="D"))).dt.days != 1).cumsum()
                    data_group = group.groupby("cycle").agg(day_count=("day", "count"), day_min=("day", "min"), day_max=("day", "max")).sort_values("day_count", ascending=False)
                    dic_data = {"user_id": name, "day_count": data_group.day_count.values[0], "day_min": data_group.day_min.values[0], "day_max": data_group.day_max.values[0]}
                    data.append(dic_data)
                data = pd.DataFrame(data)
                print(data)

            def fun2_cycle():
                """
                计算用户连续最长登录天数
                :return: dataframe，["user_id", "day_count", "day_min", "day_max"]
                """
                # 方法二：使用pandas自带的窗口函数,rank
                user_data.sort_values(by=["user_id", "day"], ascending=[True, True], inplace=True)
                user_data_group = user_data["day"] - pd.to_timedelta(user_data.groupby("user_id")["day"].rank(method="dense", ascending=True), unit='d')
                user_group = user_data.groupby(by=["user_id", user_data_group], as_index=False).agg(day_count=("day", "count"), day_min=("day", "min"), day_max=("day", "max"))
                # 筛选各分组中排名第一的一行，如果是第一，则返回ture，否则返回false，配合后面pandas过滤的特性直接筛选出各分组的第一
                mask = user_group.groupby("user_id")["day_count"].rank(method="first", ascending=False) == 1
                cycle_data = user_group[mask].sort_values(["day_count", "user_id"], ascending=[False, True])
                print(cycle_data)
                return cycle_data

            def fun3_cycle():
                """
                计算用户过去5天内登录几天，过去10天内登录几天，过去一个月内登录几天, 过去两个月登录几天
                用户活跃率分类：
                    1. 活跃用户：过去7天内登录天数>=5天
                    2. 不活跃用户：过去7天内登录天数<5天，且过去14天内登录天数>=5天
                    3. 流失用户：过去7天内无登录，且过去14天内无登录, 且过去一个月内登录天数<3天
                    4. 回流用户：过去7天内登录天数>1天，且过去14天内无登录,且过去两个月内登录天数>=3天
                :return: dataframe，["user_id", "day_count", "day_min", "day_max"]
                """
                user_data_group = user_data.groupby("user_id").agg(day_count=("day", "count"))
                today = datetime.datetime(2018, 4, 15)
                user_data_7 = user_data[user_data["day"] >= (today - datetime.timedelta(days=7))]
                user_data_14 = user_data[user_data["day"] >= (today - datetime.timedelta(days=14))]
                user_data_30 = user_data[user_data["day"] >= (today - datetime.timedelta(days=30))]
                user_data_7_group = user_data_7.groupby("user_id", as_index=False).agg(day_7=("day", "count"))
                user_data_14_group = user_data_14.groupby("user_id", as_index=False).agg(day_14=("day", "count"))
                user_data_30_group = user_data_30.groupby("user_id", as_index=False).agg(day_30=("day", "count"))
                user_cycle = pd.merge(user_data_group, user_data_7_group, on="user_id", how="left")
                user_cycle = pd.merge(user_cycle, user_data_14_group, on="user_id", how="left")
                user_cycle = pd.merge(user_cycle, user_data_30_group, on="user_id", how="left").fillna(0)
                print(user_cycle)
                return user_cycle

            user_continue = fun2_cycle()
            user_cycle = fun3_cycle()
            user_data = pd.merge(user_continue, user_cycle, on="user_id", how="right")
            # user_data.to_csv("../static/data/user_cycle.csv", index=False)
        user_views_cycle()

    """
    2.9 用户画像分析
    """
    def user_portrait(self):
        pass


def main():
    # 1. 日报数据分析
    # day_data = DayFlowData()
    # 1.1 当日会员数据
    # day_data.get_user_member("2018-03-02")
    # 1.2 当日浏览数据
    # day_data.get_user_day_flow("2018-03-02")     # 获取用户当天pv,uv数据
    # day_data.get_user_action_way()    # 获取用户当天行为数据
    # day_data.get_user_active_time("2018-03-02")       # 获取用户当前的活跃时间hour
    # 1.4 当日商品数据
    # day_data.get_product_cate("2018-03-02")
    # 1.5 保存当日数据
    # day_data.save_data("2018-03-02")

    # 2. 月流量分析
    month_data = MonthFlow()
    # month_data.read_month_action_data(2018, 3)   # 此方法是获取指定月的流量数据，将获取的数据储存在csv种，执行一次

    # 2.1 用户流量对比分析
    # month_data.user_flow_analysis(3)
    # 2.4 用户活跃率分析
    month_data.user_active_analysis(3)
    # 2.5 用户留存率分析
    # month_data.user_retention_analysis(3)
    # 2.6 用户转化率分析
    # month_data.user_conversion_rate()
    # 2.7 用户路径分析
    # month_data.user_path_analysis()
    # 2.8 用户价值分析
    # month_data.user_value_analysis()
    # 2.9 用户画像分析
    # month_data.user_portrait()


if __name__ == '__main__':
    main()
    print("程序结束！")
