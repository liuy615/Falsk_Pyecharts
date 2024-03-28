$(window).load(function(){$(".loading").fadeOut()})
$(function () {
    echarts_l2()
    echarts_l3()
    echarts_l4()
    echarts_lc2()
    echarts_lc3()
    echarts_lc4()
    echarts_cr3()
    echarts_r2()
    echarts_r3()


    // echarts_l2 是左边第二个图
    function echarts_l2() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echartl2'));
        $.ajax({
            url:"/l2",
            success: function (data) {
                option = {
                    tooltip: {
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c} ({d}%)'
                    },
                    legend: {
                        data: ['会员', '非会员', '男', '女', '未填写'],
                        textStyle: {
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 14,
                            fontWeight: 500
                        },
                    },
                    series: [
                        {
                            name: '今日浏览量',
                            type: 'pie',
                            selectedMode: 'single',
                            radius: [0, '30%'],
                            label: {
                                position: 'inner',
                                fontSize: 14
                            },
                            labelLine: {
                                show: false
                            },
                            data: [
                                { value: data["member_sum"], name: '会员' },
                                { value: data["user_sum"], name: '非会员' },
                            ]
                        },
                        {
                            name: '会员性别占比',
                            type: 'pie',
                            radius: ['45%', '60%'],
                            labelLine: {
                                length: 30
                            },
                            label: {
                                position: 'inner',
                                fontSize: 14
                            },
                            data: [
                                { value: data["man"], name: '男' },
                                { value: data["woman"], name: '女' },
                                { value: data["未知"], name: '未填写' },
                            ]
                        }
                    ]
                };
                myChart.setOption(option);
                window.addEventListener("resize",function(){
                    myChart.resize();
                });
            }
        })
    }

    // echarts_l3 是左边第三个图
    function echarts_l3() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echartl3'));
        $.ajax({
            url:"/l3",
            success: function (data) {
                option = {
                    tooltip: {
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c} ({d}%)'
                    },
                    legend: {
                        data: ['会员', '非会员', '15以下', '15-25', '25-35', '35-45', '45-55', '55以上'],
                        textStyle: {
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 14,
                            fontWeight: 500
                        },
                    },
                    series: [
                        {
                            name: '今日浏览量',
                            type: 'pie',
                            selectedMode: 'single',
                            radius: [0, '30%'],
                            label: {
                                position: 'inner',
                                fontSize: 14
                            },
                            labelLine: {
                                show: false
                            },
                            data: [
                                { value: data["member_sum"], name: '会员' },
                                { value: data["user_sum"], name: '非会员' },
                            ]
                        },
                        {
                            name: '会员年龄占比',
                            type: 'pie',
                            radius: ['45%', '60%'],
                            labelLine: {
                                length: 30
                            },
                            label: {
                                position: 'inner',
                                fontSize: 14
                            },
                            data: [
                                { value: data["15以下"], name: '15以下' },
                                { value: data["15-25"], name: '15-25' },
                                { value: data["25-35"], name: '25-35' },
                                { value: data["35-45"], name: '35-45' },
                                { value: data["45-55"], name: '45-55' },
                                { value: data["55以上"], name: '55以上' },

                            ]
                        }
                    ]
                };
                myChart.setOption(option);
                window.addEventListener("resize",function(){
                    myChart.resize();
                });
            }
        })
    }

    // echarts_l4 是左边第四个图
    function echarts_l4() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echartl4'));
        $.ajax({
            url:"/l4",
            success: function (data) {
                option = {
                    tooltip: {
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c} ({d}%)'
                    },
                    legend: {
                        data: ['会员', '非会员', '1级', '2级', '3级', '4级', '5级', '6级', '7级'],
                        textStyle: {
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 14,
                            fontWeight: 500
                        },
                    },
                    series: [
                        {
                            name: '今日浏览量',
                            type: 'pie',
                            selectedMode: 'single',
                            radius: [0, '30%'],
                            label: {
                                position: 'inner',
                                fontSize: 14
                            },
                            labelLine: {
                                show: false
                            },
                            data: [
                                { value: data["member_sum"], name: '会员' },
                                { value: data["user_sum"], name: '非会员' },
                            ]
                        },
                        {
                            name: '会员等级占比',
                            type: 'pie',
                            radius: ['45%', '60%'],
                            labelLine: {
                                length: 30
                            },
                            label: {
                                position: 'inner',
                                fontSize: 14
                            },
                            data: [
                                { value: data["member_lv_data"][0], name: data["member_lv_index"][0] + "级"},
                                { value: data["member_lv_data"][1], name: data["member_lv_index"][1] + "级"},
                                { value: data["member_lv_data"][2], name: data["member_lv_index"][2] + "级"},
                                { value: data["member_lv_data"][3], name: data["member_lv_index"][3] + "级"},
                                { value: data["member_lv_data"][4], name: data["member_lv_index"][4] + "级"},
                                { value: data["member_lv_data"][5], name: data["member_lv_index"][5] + "级"},
                            ]
                        }
                    ]
                };
                myChart.setOption(option);
                window.addEventListener("resize",function(){
                    myChart.resize();
                });
            }
        })
    }

    // echarts_lc2 是中间靠左边第2个图
    function echarts_lc2() {
            // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echartlc2'));
        $.ajax({
            url: "lc2",
            success:function (data) {
                option = {
                    color: ['#2EB7BD', '#4695D1'],
                    grid: {
                        show: false,                                   //是否显示图表背景网格
                        left: '1%',                                    //图表距离容器左侧多少距离
                        right: '1%',                                   //图表距离容器右侧侧多少距离
                        bottom: '1%',                                  //图表距离容器上面多少距离
                        top: '12%',                                    //图表距离容器下面多少距离
                        containLabel: true,                            //防止标签溢出
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        },
                    },
                    legend: {
                        orient: 'horizontal',
                        x:'center',
                        y:'top',
                        textStyle: {
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 14,
                            fontWeight: 500
                        },
                        data: ['PV', 'UV'],
                    },
                    xAxis: {
                        type: 'category',
                        nameGap:15,
                        data: data["lc2_index"],
                        axisLine:{
                            symbol: ['none','arrow'],
                            lineStyle:{
                                color: 'rgba(255,255,255,.6)',
                            }
                        }
                    },
                    yAxis: {
                        type: 'value',
                        splitLine: {show: false},
                        axisLine:{
                            symbol: ['none','arrow'],
                            lineStyle:{
                                color:'rgba(255,255,255,.6)',
                                type:'solid',
                                opacity:1
                            }
                        },
                        axisLabel:{
                            fontSize:16,
                            color:'rgba(255,255,255,.6)',
                        }
                    },
                    series: [{
                        name: 'PV',
                        data: data["lc2_pv"],
                        type: 'bar',
                        label: {
                            show: true,
                            position: 'top'
                        }
                    }, {
                        name: 'UV',
                        data: data["lc2_uv"],
                        type: 'bar',
                        label: {
                            show: true,
                            position: 'top'
                        }
                    }]
                };
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
                // 让图表跟随屏幕自适应大小
                window.addEventListener("resize",function(){
                    myChart.resize();
                });
            }
        })
    }

    // echarts_lc3 是中间靠左边第3个图
    function echarts_lc3() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echartlc3'));
        $.ajax({
            url: "lc3",
            success:function (data) {
                option = {
                    series: {
                        type: 'sankey',
                        layout: 'none',
                        emphasis: {
                            focus: 'adjacency'
                        },
                        data: [{
                                name: '浏览'
                            }, {
                                name: '加购'
                            }, {
                                name: '收藏'
                            }, {
                                name: '下单'
                            }],
                        links: [{
                                source: '浏览',
                                target: '加购',
                                value: data["browse_add"]
                            }, {
                                source: '浏览',
                                target: '收藏',
                                value: data["browse_save"]
                            }, {
                                source: '浏览',
                                target: '下单',
                                value: data["browse_buy"]
                            },{
                                source: '加购',
                                target: '收藏',
                                value: data["add_save"]
                            }, {
                                source: '加购',
                                target: '下单',
                                value: data["add_buy"]
                            }, {
                                source: '收藏',
                                target: '下单',
                                value: data["save_buy"]
                        }],
                        lineStyle: {
                            normal: {
                                color: 'red',
                                curveness: .5
                            }
                        },
                        itemStyle: {
                            normal: {
                                borderWidth: 1,
                                borderColor: '#aaa'
                            }
                        },
                    }
                };
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
                // 让图表跟随屏幕自适应大小
                window.addEventListener("resize",function(){
                    myChart.resize();
                });
            }
        })
    }

    // echarts_lc4 是中间靠左边第4个图
    function echarts_lc4() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echartlc4'));
        $.ajax({
            url: "lc4",
            success:function (data) {
                color: ['#2EB7BD', '#4695D1'],
                option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        },
                    },
                    grid: {
                        show: false,                                   //是否显示图表背景网格
                        left: '1%',                                    //图表距离容器左侧多少距离
                        right: '7%',                                   //图表距离容器右侧侧多少距离
                        bottom: '1%',                                  //图表距离容器上面多少距离
                        top: '12%',                                    //图表距离容器下面多少距离
                        containLabel: true,                            //防止标签溢出
                    },
                    legend: {
                        data: ['流量活跃时段', '用户活跃时段'],
                        textStyle:{
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 16,
                        }
                    },
                    calculable: true,
                    xAxis: {
                        type: 'category',
                        data: data["lc4_index"],
                        splitLine: {show: false},
                        axisLine: {
                            symbol: ['none','arrow'],
                            lineStyle:{
                                color:'rgba(255,255,255,.6)',
                                type:'solid',
                                opacity:1
                            }
                        },
                        axisLabel:{
                            fontSize:16,
                            color:'rgba(255,255,255,.6)',
                        }
                    },
                    yAxis: {
                        type: 'value',
                        splitLine: {show: false},
                        axisLine: {
                            symbol: ['none', 'arrow'],
                            lineStyle: {
                                color: 'rgba(255,255,255,.6)',
                                type: 'solid',
                                opacity: 1
                            }
                        },
                        axisLabel:{
                            fontSize:16,
                            color:'rgba(255,255,255,.6)',
                        }
                    },
                    series: [{
                        name: '流量活跃时段',
                        type: 'bar',
                        data: data["lc4_pv"],
                        itemStyle: {
                            normal: {
                                color: '#2EB7BD'
                            },
                        },
                        markPoint: {
                            data: [
                                { type: 'max', name: 'Max' },
                                { type: 'min', name: 'Min' }],
                            },
                        markLine: {data: [{ type: 'average', name: 'Avg' }]}
                        }, {
                        name: '用户活跃时段',
                        type: 'bar',
                        data:data["lc4_uv"],
                        itemStyle: {
                            normal: {
                                color: '#4695D1'
                            },
                        },
                        markPoint: {
                            data: [
                                { type: 'max', name: 'Max'},
                                { type: 'min', name: 'Min'}]
                            },
                        markLine: {data: [{ type: 'average', name: 'Avg' }]}
                        }
                    ]
                };
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
                // 让图表跟随屏幕自适应大小
                window.addEventListener("resize",function(){
                    myChart.resize();
                });
            }
        })
    }

    // echarts_cr3是中间靠右第三个图
    function echarts_cr3() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echartcr3'));
        $.ajax({
            url:"/cr3",
            success:function (data) {
                option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            lineStyle: {
                                color: '#dddc6b'
                            }
                        }
                    },
                    grid: {
                        left: '10',
                        top: '20',
                        right: '30',
                        bottom: '10',
                        containLabel: true
                    },
                    xAxis: [{
                        type: 'category',
                        boundaryGap: false,
                        axisLabel:  {
                            textStyle: {
                            color: "rgba(255,255,255,.6)",
                            fontSize:14,
                             },
                         },
                        axisLine: {
                            lineStyle: {
                                color: 'rgba(255,255,255,.2)'
                            }
                        },
                    data: data["日期"]
                    },
                    {
                        axisPointer: {show: false},
                        axisLine: {  show: false},
                        position: 'bottom',
                        offset: 20,
                    }],
                    yAxis: [{
                        type: 'value',
                        axisTick: {show: false},
                        splitNumber: 4,
                        axisLine: {
                            lineStyle: {
                                color: 'rgba(255,255,255,.1)'
                            }
                        },
                        axisLabel:  {
                           textStyle: {
                                color: "rgba(255,255,255,.6)",
                                fontSize:16,
                           },
                        },
                        splitLine: {
                            lineStyle: {
                                color: 'rgba(255,255,255,.1)',
                                type: 'dotted',
                            }
                        }
                    }],
                    series: [{
                        name: '每年新增会员数',
                        type: 'line',
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 5,
                        showSymbol: false,
                        lineStyle: {
                            normal: {
                                color: 'rgba(31, 174, 234, 1)',
                                width: 2
                            }
                        },
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgba(31, 174, 234, 0.4)'
                                },
                                {
                                    offset: 0.8,
                                    color: 'rgba(31, 174, 234, 0.1)'
                                }], false),
                                shadowColor: 'rgba(0, 0, 0, 0.1)',
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: '#1f7eea',
                                borderColor: 'rgba(31, 174, 234, .1)',
                                borderWidth: 5
                            }
                        },
                        data: data["num"]
                    }]
                };
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
                window.addEventListener("resize",function(){
                    myChart.resize();
                });
            }
        })
    }

    // echatrs_r2是右边第二个图
    function echarts_r2() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echartr2'));
        $.ajax({
            url: "/r2",
            success: function (data) {
                const builderJson = {
                    charts: data["cate"],
                    components: data["sale_cate"],
                };
                const downloadJson = data["cate_top3"];
                const themeJson = data["sale_cate_top3"];
                color: ['#2EB7BD', '#4695D1'],
                option = {
                    tooltip: {},
                    title: [
                        {
                            text: '在线构建',
                            left: '30%',
                            textAlign: 'center',
                            textStyle: {
                                color: 'rgba(255,255,255,.6)',
                            },
                        },
                        {
                            text: '各版本下载',
                            left: '80%',
                            textAlign: 'center',
                            textStyle: {
                                color: 'rgba(255,255,255,.6)',
                            },
                        },
                        {
                            text: '主题下载',
                            left: '80%',
                            top: '50%',
                            textAlign: 'center',
                            textStyle: {
                                color: 'rgba(255,255,255,.6)',
                            },
                        }
                    ],
                    grid: [
                        {
                            top: '5%',
                            width: '60%',
                            bottom: '45%',
                            left: 5,
                            containLabel: true
                        },
                        {
                            top: '55%',
                            width: '60%',
                            bottom: 0,
                            left: 5,
                            containLabel: true
                        }
                    ],
                    xAxis: [
                        {
                            type: 'value',
                            splitLine: {show: false},
                            axisLabel: {
                                interval: 0,
                                fontSize:12,
                                color:'rgba(255,255,255,.6)',
                            },
                            axisLine:{
                                symbol: ['none','arrow'],
                                lineStyle:{
                                    color: 'rgba(255,255,255,.6)',
                                }
                            }
                        },
                        {
                            type: 'value',
                            gridIndex: 1,
                            splitLine: {show: false},
                            axisLabel: {
                                interval: 0,
                                fontSize:12,
                                color:'rgba(255,255,255,.6)',
                            },
                            axisLine:{
                                symbol: ['none','arrow'],
                                lineStyle:{
                                    color: 'rgba(255,255,255,.6)',
                                }
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'category',
                            data: Object.keys(builderJson.charts),
                            axisLabel: {
                                interval: 0,
                                rotate: 30,
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine:{
                                symbol: ['none','arrow'],
                                lineStyle:{
                                    color: 'rgba(255,255,255,.6)',
                                }
                            },
                        },
                        {
                            gridIndex: 1,
                            type: 'category',
                            data: Object.keys(builderJson.components),
                            axisLabel: {
                                interval: 0,
                                rotate: 30,
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine:{
                                symbol: ['none','arrow'],
                                lineStyle:{
                                    color: 'rgba(255,255,255,.6)',
                                }
                            }
                        }
                    ],
                    series: [
                        {
                            type: 'bar',
                            stack: 'chart',
                            z: 3,
                            label: {
                                position: 'right',
                                show: true
                            },
                            itemStyle: {
                                normal: {
                                    color: '#2EB7BD'
                                },
                            },
                            data: Object.keys(builderJson.charts).map(function (key) {
                                return builderJson.charts[key];
                            })
                        },
                        {
                            type: 'bar',
                            stack: 'component',
                            xAxisIndex: 1,
                            yAxisIndex: 1,
                            z: 3,
                            label: {
                                position: 'right',
                                show: true
                            },
                            itemStyle: {
                                normal: {
                                    color: '#4695D1'
                                },
                            },
                            data: Object.keys(builderJson.components).map(function (key) {
                                return builderJson.components[key];
                            })
                        },
                        {
                            type: 'pie',
                            radius: [0, '30%'],
                            center: ['80%', '25%'],
                            label: {                //echarts饼图内部显示百分比设置
                                show: true,
                                position: "inside", //outside 外部显示  inside 内部显示
                                formatter: `{d}%`,
                                color: "#ffffff", //颜色
                                fontSize: 12 //字体大小
                            },
                            data: Object.keys(downloadJson).map(function (key) {
                                return {
                                    name: key,
                                    value: downloadJson[key]
                                };
                            })
                        },
                        {
                            type: 'pie',
                            radius: [0, '30%'],
                            center: ['80%', '75%'],
                            label: {
                                show: true,
                                position: "inside", //outside 外部显示  inside 内部显示
                                formatter: `{d}%`,
                                color: "#ffffff", //颜色
                                fontSize: 12 //字体大小
                            },
                            data: Object.keys(themeJson).map(function (key) {
                                return {
                                    name: key,
                                    value: themeJson[key]
                                };
                            })
                        }
                    ]
                };
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
                window.addEventListener("resize",function(){
                    myChart.resize();
                });
            }
        })
    }

    // echatrs_r3 是右边第三个图
    function echarts_r3() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echartr3'));
        $.ajax({
            url: "/r3",
            success: function (data) {
                const builderJson = {
                    charts: data["cate"],
                    components: data["sale_cate"],
                };
                const downloadJson = data["cate_top3"];
                const themeJson = data["sale_cate_top3"];
                color: ['#2EB7BD', '#4695D1'],
                    option = {
                        tooltip: {},
                        title: [
                            {
                                text: '在线构建',
                                left: '30%',
                                textAlign: 'center',
                                textStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                },

                            },
                            {
                                text: '各版本下载',
                                left: '80%',
                                textAlign: 'center',
                                textStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                },
                            },
                            {
                                text: '主题下载',
                                left: '80%',
                                top: '50%',
                                textAlign: 'center',
                                textStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                },
                            }
                        ],
                        grid: [
                            {
                                top: '5%',
                                width: '60%',
                                bottom: '45%',
                                left: 5,
                                containLabel: true
                            },
                            {
                                top: '55%',
                                width: '60%',
                                bottom: 0,
                                left: 5,
                                containLabel: true
                            }
                        ],
                        xAxis: [
                            {
                                type: 'value',
                                splitLine: {show: false},
                                axisLabel: {
                                    interval: 0,
                                    fontSize:12,
                                    color:'rgba(255,255,255,.6)',
                                },
                                axisLine:{
                                    symbol: ['none','arrow'],
                                    lineStyle:{
                                        color: 'rgba(255,255,255,.6)',
                                    }
                                }
                            },
                            {
                                type: 'value',
                                gridIndex: 1,
                                splitLine: {show: false},
                                axisLabel: {
                                    interval: 0,
                                    fontSize:12,
                                    color:'rgba(255,255,255,.6)',
                                },
                                axisLine:{
                                    symbol: ['none','arrow'],
                                    lineStyle:{
                                        color: 'rgba(255,255,255,.6)',
                                    }
                                }
                            }
                        ],
                        yAxis: [
                            {
                                type: 'category',
                                data: Object.keys(builderJson.charts),
                                axisLabel: {
                                    interval: 0,
                                    rotate: 30,
                                    fontSize:14,
                                    color:'rgba(255,255,255,.6)',
                                },
                                splitLine: {show: false},
                                axisLine:{
                                    symbol: ['none','arrow'],
                                    lineStyle:{
                                        color: 'rgba(255,255,255,.6)',
                                    }
                                },
                            },
                            {
                                gridIndex: 1,
                                type: 'category',
                                data: Object.keys(builderJson.components),
                                axisLabel: {
                                    interval: 0,
                                    rotate: 30,
                                    fontSize:14,
                                    color:'rgba(255,255,255,.6)',
                                },
                                splitLine: {show: false},
                                axisLine:{
                                    symbol: ['none','arrow'],
                                    lineStyle:{
                                        color: 'rgba(255,255,255,.6)',
                                    }
                                }
                            }
                        ],
                        series: [
                            {
                                type: 'bar',
                                stack: 'chart',
                                z: 3,
                                label: {
                                    position: 'right',
                                    show: true
                                },
                                itemStyle: {
                                    normal: {
                                        color: '#2EB7BD'
                                    },
                                },
                                data: Object.keys(builderJson.charts).map(function (key) {
                                    return builderJson.charts[key];
                                })
                            },
                            {
                                type: 'bar',
                                stack: 'component',
                                xAxisIndex: 1,
                                yAxisIndex: 1,
                                z: 3,
                                label: {
                                    position: 'right',
                                    show: true
                                },
                                itemStyle: {
                                    normal: {
                                        color: '#4695D1'
                                    },
                                },
                                data: Object.keys(builderJson.components).map(function (key) {
                                    return builderJson.components[key];
                                })
                            },
                            {
                                type: 'pie',
                                radius: [0, '30%'],
                                center: ['80%', '25%'],
                                label: {                //echarts饼图内部显示百分比设置
                                    show: true,
                                    position: "inside", //outside 外部显示  inside 内部显示
                                    formatter: `{d}%`,
                                    color: "#ffffff", //颜色
                                    fontSize: 12 //字体大小
                                },
                                data: Object.keys(downloadJson).map(function (key) {
                                    return {
                                        name: key,
                                        value: downloadJson[key]
                                    };
                                })
                            },
                            {
                                type: 'pie',
                                radius: [0, '30%'],
                                center: ['80%', '75%'],
                                label: {                //echarts饼图内部显示百分比设置
                                    show: true,
                                    position: "inside", //outside 外部显示  inside 内部显示
                                    formatter: `{d}%`,
                                    color: "#ffffff", //颜色
                                    fontSize: 12 //字体大小
                                },
                                data: Object.keys(themeJson).map(function (key) {
                                    return {
                                        name: key,
                                        value: themeJson[key]
                                    };
                                })
                            }
                        ]
                    };
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
                window.addEventListener("resize",function(){
                    myChart.resize();
                });
            }
        })
    }

})



		
		
		


		









