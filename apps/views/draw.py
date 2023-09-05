# -*- coding: utf-8 -*
# @Time    : 2023/6/28 11:25
# @Author  : liuy
# @File    : draw.py
import pandas as pd
from pyecharts.charts import Line, Bar, Page, Funnel
from pyecharts import options as opts
from bs4 import BeautifulSoup
from tools import get_rate_increase


# 月流量分析
class MonthFlow:
    def pv_data(self, last_read_path, read_path, sava_path):
        """
        此方法用于将月流量pv数据转化为可视化的图形
        """
        # PV日流量折线图
        last_pv_day_data = pd.read_excel(last_read_path, sheet_name="pv_day_data")  # 上个月的日pv数据
        pv_day_data = pd.read_excel(read_path, sheet_name="pv_day_data")  # 这个月的日pv数据
        pv_day_x = [str(i) for i in pv_day_data["day"]]  # 横坐标数据，以这个月的日期为准
        last_pv_day_y = last_pv_day_data["num"].tolist()
        pv_day_y = pv_day_data["num"].tolist()
        pv_day_line = (
            Line()
            .add_xaxis(pv_day_x)
            .add_yaxis("上月", last_pv_day_y, label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("本月", pv_day_y, label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts("PV日流量折线图"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            )
        )
        # PV周流量柱状图
        last_pv_week_data = pd.read_excel(last_read_path, sheet_name="pv_week_data")
        pv_week_data = pd.read_excel(read_path, sheet_name="pv_week_data")
        pv_week_x = [str(i) for i in pv_week_data["week"]]
        last_pv_week_y = last_pv_week_data["num"].tolist()
        pv_week_y = pv_week_data["num"].tolist()
        pv_week_bar = (
            Bar()
            .add_xaxis(pv_week_x)
            .add_yaxis("上月", last_pv_week_y, yaxis_index=0, category_gap="50%", label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("本月", pv_week_y, yaxis_index=0, category_gap="50%", label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts("PV周流量柱状图"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            )
            .extend_axis(   # 第二坐标轴
                yaxis=opts.AxisOpts(
                    name="增长率",
                    type_="value",
                    interval=10,
                    axislabel_opts=opts.LabelOpts(formatter="{value} %")  # 设置坐标轴格式
                )
            )
        )
        pv_week_rate = get_rate_increase(last_pv_week_data, pv_week_data)
        pv_week_line = (
            Line()
            .add_xaxis(pv_week_x)
            .add_yaxis("增长率", pv_week_rate.to_list(), yaxis_index=1, label_opts=opts.LabelOpts(is_show=False))
        )
        pv_week_bar.overlap(pv_week_line)
        # PV时流量柱状图
        last_pv_hour_data = pd.read_excel(last_read_path, sheet_name="pv_hour_data")
        pv_hour_data = pd.read_excel(read_path, sheet_name="pv_hour_data")
        pv_hour_x = [str(i) for i in pv_hour_data["hour"]]
        last_pv_hour_y = last_pv_hour_data["num"].tolist()
        pv_hour_y = pv_hour_data["num"].tolist()
        pv_hour_bar = (
            Bar()
            .add_xaxis(pv_hour_x)
            .add_yaxis("上月", last_pv_hour_y, category_gap="50%", gap="0%", label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("本月", pv_hour_y, category_gap="50%", gap="0%", label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts("PV时流量柱状图"),
                datazoom_opts=opts.DataZoomOpts(is_show=True),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            )
            .extend_axis(   # 第二坐标轴
                yaxis=opts.AxisOpts(
                    name="增长率",
                    type_="value",
                    interval=10,
                    axislabel_opts=opts.LabelOpts(formatter="{value} %")  # 设置坐标轴格式
                )
            )
        )
        pv_hour_rate = get_rate_increase(last_pv_hour_data, pv_hour_data)
        pv_hour_line = (
            Line()
            .add_xaxis(pv_hour_x)
            .add_yaxis("增长率", pv_hour_rate.to_list(), yaxis_index=1, label_opts=opts.LabelOpts(is_show=False))
        )
        pv_hour_bar.overlap(pv_hour_line)

        # PV漏斗图
        pv_type_data = pd.read_excel(read_path, sheet_name="pv_type_data")
        pv_tpye_x = ["浏览", "下单", "关注", "评论"]
        pv_tpye_y = pv_type_data["num"].tolist()
        pv_type_fun = (
            Funnel()
            .add("类别", [list(z) for z in zip(pv_tpye_x, pv_tpye_y)])
            .set_global_opts(
                title_opts=opts.TitleOpts("PV转化率漏斗图")
            )
        )
        pv_page = (
                Page()
                .add(pv_day_line)
                .add(pv_week_bar)
                .add(pv_hour_bar)
                .add(pv_type_fun)
            )
        pv_page.render(sava_path)
        with open(sava_path, "r+", encoding='utf-8') as html:
            html_bf = BeautifulSoup(html, 'lxml')
            divs = html_bf.select('.chart-container')
            divs[0]["style"] = "width:50%;height:50%;position:absolute;top:0;left:25%;"
            divs[1]["style"] = "width:50%;height:50%;position:absolute;top:50%;left:25%;"
            divs[2]["style"] = "width:50%;height:50%;position:absolute;top:100%;left:25%;"
            divs[3]["style"] = "width:50%;height:50%;position:absolute;top:150%;left:25%;"
            html_new = str(html_bf)
            html.seek(0, 0)
            html.truncate()
            html.write(html_new)

    def uv_data(self, last_read_path, read_path, sava_path):
        """
        此方法用于将月流量uv数据转化为可视化的图形
        """
        # UV日流量折线图
        last_uv_day_data = pd.read_excel(last_read_path, sheet_name="uv_day_data")
        uv_day_data = pd.read_excel(read_path, sheet_name="uv_day_data")
        uv_day_x = [str(i) for i in uv_day_data["day"]]
        last_uv_day_y = last_uv_day_data["num"].tolist()
        uv_day_y = uv_day_data["num"].tolist()
        uv_day_line = (
            Line()
            .add_xaxis(uv_day_x)
            .add_yaxis("上月", last_uv_day_y, label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("本月", uv_day_y, label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts("UV日流量折线图"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            )
        )
        # UV周流量柱状图
        last_uv_week_data = pd.read_excel(last_read_path, sheet_name="uv_week_data")
        uv_week_data = pd.read_excel(read_path, sheet_name="uv_week_data")
        uv_week_x = [str(i) for i in uv_week_data["week"]]
        last_uv_week_y = last_uv_week_data["num"].tolist()
        uv_week_y = uv_week_data["num"].tolist()
        uv_week_bar = (
            Bar()
            .add_xaxis(uv_week_x)
            .add_yaxis("上月", last_uv_week_y, category_gap="50%", label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("本月", uv_week_y, category_gap="50%", label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts("UV周流量柱状图"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            )
            .extend_axis(   # 第二坐标轴
                yaxis=opts.AxisOpts(
                    name="增长率",
                    type_="value",
                    interval=10,
                    axislabel_opts=opts.LabelOpts(formatter="{value} %")  # 设置坐标轴格式
                )
            )
        )
        uv_week_rate = get_rate_increase(last_uv_week_data, uv_week_data)
        uv_week_line = (
            Line()
            .add_xaxis(uv_week_x)
            .add_yaxis("增长率", uv_week_rate.to_list(), yaxis_index=1, label_opts=opts.LabelOpts(is_show=False))
        )
        uv_week_bar.overlap(uv_week_line)

        # UV时流量柱状图
        last_uv_hour_data = pd.read_excel(last_read_path, sheet_name="uv_hour_data")
        uv_hour_data = pd.read_excel(read_path, sheet_name="uv_hour_data")
        uv_hour_x = [str(i) for i in uv_hour_data["hour"]]
        last_uv_hour_y = last_uv_hour_data["num"].tolist()
        uv_hour_y = uv_hour_data["num"].tolist()
        uv_hour_bar = (
            Bar()
            .add_xaxis(uv_hour_x)
            .add_yaxis("上月", last_uv_hour_y, category_gap="50%", gap="0%", label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("本月", uv_hour_y, category_gap="50%", gap="0%", label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts("UV时流量柱状图"),
                datazoom_opts=opts.DataZoomOpts(is_show=True),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            )
            .extend_axis(   # 第二坐标轴
                yaxis=opts.AxisOpts(
                    name="增长率",
                    type_="value",
                    interval=10,
                    axislabel_opts=opts.LabelOpts(formatter="{value} %")  # 设置坐标轴格式
                )
            )
        )
        uv_hour_rate = get_rate_increase(last_uv_hour_data, uv_hour_data)
        uv_hour_line = (
            Line()
            .add_xaxis(uv_hour_x)
            .add_yaxis("增长率", uv_hour_rate.to_list(), yaxis_index=1, label_opts=opts.LabelOpts(is_show=False))
        )
        uv_hour_bar.overlap(uv_hour_line)

        # UV漏斗图
        uv_type_data = pd.read_excel(read_path, sheet_name="uv_type_data")
        uv_tpye_x = ["浏览", "下单", "关注", "评论"]
        uv_tpye_y = uv_type_data["num"].tolist()
        uv_type_fun = (
            Funnel()
            .add("类别", [list(z) for z in zip(uv_tpye_x, uv_tpye_y)])
            .set_global_opts(
                title_opts=opts.TitleOpts("UV转化率漏斗图")
            )
        )
        uv_page = (
            Page()
            .add(uv_day_line)
            .add(uv_week_bar)
            .add(uv_hour_bar)
            .add(uv_type_fun)
        )
        uv_page.render(sava_path)
        with open(sava_path, "r+", encoding='utf-8') as html:
            html_bf = BeautifulSoup(html, 'lxml')
            divs = html_bf.select('.chart-container')
            divs[0]["style"] = "width:50%;height:50%;position:absolute;top:0;left:25%;"
            divs[1]["style"] = "width:50%;height:50%;position:absolute;top:50%;left:25%;"
            divs[2]["style"] = "width:50%;height:50%;position:absolute;top:100%;left:25%;"
            divs[3]["style"] = "width:50%;height:50%;position:absolute;top:150%;left:25%;"
            html_new = str(html_bf)
            html.seek(0, 0)
            html.truncate()
            html.write(html_new)


def user_portrait_data(read_path, sava_path):
    data = pd.read_excel(read_path, sheet_name="user_portrait_data", index_col=None)
    print(data)


def main():
    # 3月流量数据绘图
    month_flow = MonthFlow()
    month_flow.pv_data("../static/2月数据/month_pv_data.xlsx", "../static/3月数据/month_pv_data.xlsx", "../templates/3月可视化/2018_3_pv.html")
    month_flow.uv_data("../static/2月数据/month_uv_data.xlsx", "../static/3月数据/month_uv_data.xlsx", "../templates/3月可视化/2018_3_uv.html")


if __name__ == '__main__':
    main()
    print("程序结束！")
