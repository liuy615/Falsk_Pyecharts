# -*- coding: utf-8 -*
# @Time    : 2023/6/28 11:25
# @Author  : liuy
# @File    : draw.py
import pandas as pd
from pyecharts.charts import Line, Bar, Page, Tab
from pyecharts import options as opts
from bs4 import BeautifulSoup


# 月流量分析
def flow_data(read_path, sava_path):
    # PV日流量折线图
    pv_day_data = pd.read_excel(read_path, sheet_name="pv_day_data")
    pv_day_x = [str(i) for i in pv_day_data["day"]]
    pv_day_y = pv_day_data["num"].tolist()
    pv_day_line = (
        Line()
        .add_xaxis(pv_day_x)
        .add_yaxis("人数", pv_day_y, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts("PV日流量折线图"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )
    # PV周流量柱状图
    pv_week_data = pd.read_excel(read_path, sheet_name="pv_week_data")
    pv_week_x = [str(i) for i in pv_week_data["week"]]
    pv_week_y = pv_week_data["num"].tolist()
    pv_week_bar = (
        Bar()
        .add_xaxis(pv_week_x)
        .add_yaxis("人数", pv_week_y, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("PV周流量柱状图"))
    )
    # PV时流量柱状图
    pv_hour_data = pd.read_excel(read_path, sheet_name="pv_hour_data")
    pv_hour_x = [str(i) for i in pv_hour_data["hour"]]
    pv_hour_y = pv_hour_data["num"].tolist()
    pv_hour_bar = (
        Bar()
        .add_xaxis(pv_hour_x)
        .add_yaxis("人数", pv_hour_y, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("PV时流量柱状图"))
    )
    # UV日流量折线图
    uv_day_data = pd.read_excel(read_path, sheet_name="uv_day_data")
    uv_day_x = [str(i) for i in uv_day_data["day"]]
    uv_day_y = uv_day_data["num"].tolist()
    uv_day_line = (
        Line()
        .add_xaxis(uv_day_x)
        .add_yaxis("人数", uv_day_y, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts("UV日流量折线图"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )
    # UV周流量柱状图
    uv_week_data = pd.read_excel(read_path, sheet_name="uv_week_data")
    uv_week_x = [str(i) for i in uv_week_data["week"]]
    uv_week_y = uv_week_data["num"].tolist()
    uv_week_bar = (
        Bar()
        .add_xaxis(uv_week_x)
        .add_yaxis("人数", uv_week_y, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("UV周流量柱状图"))
    )
    # UV时流量柱状图
    uv_hour_data = pd.read_excel(read_path, sheet_name="uv_hour_data")
    uv_hour_x = [str(i) for i in uv_hour_data["hour"]]
    uv_hour_y = uv_hour_data["num"].tolist()
    uv_hour_bar = (
        Bar()
        .add_xaxis(uv_hour_x)
        .add_yaxis("人数", uv_hour_y, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("UV时流量柱状图"))
    )

    month_page = (
        Page()
        .add(pv_day_line)
        .add(pv_week_bar)
        .add(pv_hour_bar)
        .add(uv_day_line)
        .add(uv_week_bar)
        .add(uv_hour_bar)
        .render(sava_path)
    )

    with open(sava_path, "r+", encoding='utf-8') as html:
        html_bf = BeautifulSoup(html, 'lxml')
        divs = html_bf.select('.chart-container')
        divs[0]["style"] = "width:50%;height:50%;position:absolute;top:0;left:0%;"
        divs[1]["style"] = "width:50%;height:50%;position:absolute;top:50%;left:0%;"
        divs[2]["style"] = "width:50%;height:50%;position:absolute;top:100%;left:0%;"
        divs[3]["style"] = "width:50%;height:50%;position:absolute;top:0;left:50%;"
        divs[4]["style"] = "width:50%;height:50%;position:absolute;top:50%;left:50%;"
        divs[5]["style"] = "width:50%;height:50%;position:absolute;top:100%;left:50%;"
        html_new = str(html_bf)
        html.seek(0, 0)
        html.truncate()
        html.write(html_new)


if __name__ == '__main__':
    print("程序结束！")
