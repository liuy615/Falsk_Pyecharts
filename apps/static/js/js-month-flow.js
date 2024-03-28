$(window).load(function(){
    $(".loading").fadeOut()
})
			
/****/
$(document).ready(function(){
	var whei=$(window).width()
	$("html").css({fontSize:whei/20})
	$(window).resize(function(){
		var whei=$(window).width()
	 $("html").css({fontSize:whei/20})
    });
});
$(window).load(function(){$(".loading").fadeOut()})


$(function () {
    echarts_l1()
    echarts_l2()
    echarts_l3()
    echarts_c1()
    echarts_c2()
    echarts_r1()
    echarts_r2()
    echarts_r3()
    pe01()
    pe02()
    pe03()

    // 左边第一个可视化图表
    function echarts_l1() {
        var myChart = echarts.init(document.getElementById('echarts-l1'));
        $.ajax({
            url: '/month_flow_l1',
            success: function (data) {
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
                        right: '1%',                                   //图表距离容器右侧侧多少距离
                        bottom: '1%',                                  //图表距离容器上面多少距离
                        top: '15%',                                    //图表距离容器下面多少距离
                        containLabel: true,                            //防止标签溢出
                    },
                    legend: {
                        data: ['2月', '3月', '增长率'],
                        textStyle:{
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 14,
                        }
                    },
                    xAxis: [
                        {
                            type: 'category',
                            data: data["pv_day_index"],
                            axisPointer: {
                                type: 'shadow'
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none','arrow'],
                                lineStyle: {
                                    color: 'rgba(255, 255, 255, .6)',
                                }
                            },
                            axisLabel: {
                                fontSize: 14,
                                color: 'rgba(255, 255, 255, .6)'
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '浏览量(单位：k)',
                            scale: true,
                            axisLabel: {
                                formatter: '{value}',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none', 'arrow'],
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                }
                            },
                        },
                        {
                            type: 'value',
                            name: '增长率',
                            scale: true,
                            axisLabel: {
                                formatter: '{value} %',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                },
                            },
                        },
                    ],
                    series: [
                        {
                            name: '2月',
                            type: 'bar',
                            data: data["last_pv_day_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
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
                        },
                        {
                            name: '3月',
                            type: 'bar',
                            data: data["pv_day_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#4695D1'
                                },
                            },
                            markPoint: {
                                data: [
                                    { type: 'max', name: 'Max' },
                                    { type: 'min', name: 'Min' }],
                            },
                        },
                        {
                            name: '增长率',
                            type: 'line',
                            yAxisIndex: 1,
                            data: data["pv_day_rate"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + '%';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#6EB7BD'
                                },
                            },
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

    // 左边第二个可视化图表
    function echarts_l2() {
    // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echarts-l2'));
        $.ajax({
            url: '/month_flow_l2',
            success: function (data) {
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
                        right: '1%',                                   //图表距离容器右侧侧多少距离
                        bottom: '1%',                                  //图表距离容器上面多少距离
                        top: '15%',                                    //图表距离容器下面多少距离
                        containLabel: true,                            //防止标签溢出
                    },
                    legend: {
                        data: ['2月', '3月', '增长率'],
                        textStyle:{
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 14,
                        }
                    },
                    xAxis: [
                        {
                            type: 'category',
                            data: data["pv_hour_index"],
                            axisPointer: {
                                type: 'shadow'
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none','arrow'],
                                lineStyle: {
                                    color: 'rgba(255, 255, 255, .6)',
                                }
                            },
                            axisLabel: {
                                fontSize: 14,
                                color: 'rgba(255, 255, 255, .6)'
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '浏览量(单位：k)',
                            scale: true,
                            axisLabel: {
                                formatter: '{value}',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none', 'arrow'],
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                }
                            },
                        },
                        {
                            type: 'value',
                            name: '增长率',
                            scale: true,
                            axisLabel: {
                                formatter: '{value} %',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                },
                            },
                        },
                    ],
                    series: [
                        {
                            name: '2月',
                            type: 'bar',
                            data: data["last_pv_hour_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
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
                        },
                        {
                            name: '3月',
                            type: 'bar',
                            data: data["pv_hour_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#4695D1'
                                },
                            },
                            markPoint: {
                                data: [
                                    { type: 'max', name: 'Max' },
                                    { type: 'min', name: 'Min' }],
                            },
                        },
                        {
                            name: '增长率',
                            type: 'line',
                            yAxisIndex: 1,
                            data: data["pv_hour_rate"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + '%';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#6EB7BD'
                                },
                            },
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

    // 左边第三个可视化图表
    function echarts_l3() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echarts-l3'));
        $.ajax({
            url: '/month_flow_l3',
            success: function (data) {
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
                        right: '1%',                                   //图表距离容器右侧侧多少距离
                        bottom: '1%',                                  //图表距离容器上面多少距离
                        top: '15%',                                    //图表距离容器下面多少距离
                        containLabel: true,                            //防止标签溢出
                    },
                    legend: {
                        data: ['2月', '3月', '增长率'],
                        textStyle:{
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 14,
                        }
                    },
                    xAxis: [
                        {
                            type: 'category',
                            data: data["pv_week_index"],
                            axisPointer: {
                                type: 'shadow'
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none','arrow'],
                                lineStyle: {
                                    color: 'rgba(255, 255, 255, .6)',
                                }
                            },
                            axisLabel: {
                                fontSize: 14,
                                color: 'rgba(255, 255, 255, .6)'
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '浏览量(单位：k)',
                            scale: true,
                            axisLabel: {
                                formatter: '{value}',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none', 'arrow'],
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                }
                            },
                        },
                        {
                            type: 'value',
                            name: '增长率',
                            scale: true,
                            axisLabel: {
                                formatter: '{value} %',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                },
                            },
                        },
                    ],
                    series: [
                        {
                            name: '2月',
                            type: 'bar',
                            data: data["last_pv_week_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
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
                        },
                        {
                            name: '3月',
                            type: 'bar',
                            data: data["pv_week_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#4695D1'
                                },
                            },
                            markPoint: {
                                data: [
                                    { type: 'max', name: 'Max' },
                                    { type: 'min', name: 'Min' }],
                            },
                        },
                        {
                            name: '增长率',
                            type: 'line',
                            yAxisIndex: 1,
                            data: data["pv_week_rate"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + '%';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#6EB7BD'
                                },
                            },
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

    // 中间第一个可视化图表
    function echarts_c1() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echarts-c1'));
        $.ajax({
            url: '/l2',
            success: function (data) {
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
                            right: '1%',                                   //图表距离容器右侧侧多少距离
                            bottom: '1%',                                  //图表距离容器上面多少距离
                            top: '15%',                                    //图表距离容器下面多少距离
                            containLabel: true,                            //防止标签溢出
                        },
                        legend: {
                            data: ['2月', '3月', '增长率'],
                            textStyle:{
                                color: 'rgba(255,255,255,.6)',
                                fontSize: 14,
                            }
                        },
                        xAxis: [
                            {
                                type: 'category',
                                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                                axisPointer: {
                                    type: 'shadow'
                                },
                                splitLine: {show: false},
                                axisLine: {
                                    symbol: ['none','arrow'],
                                    lineStyle: {
                                        color: 'rgba(255, 255, 255, .6)',
                                    }
                                },
                                axisLabel: {
                                    fontSize: 14,
                                    color: 'rgba(255, 255, 255, .6)'
                                }
                            }
                        ],
                        yAxis: [
                            {
                                type: 'value',
                                name: '浏览量',
                                min: 0,
                                max: 250,
                                interval: 50,
                                axisLabel: {
                                    formatter: '{value} ',
                                    fontSize:14,
                                    color:'rgba(255,255,255,.6)',
                                },
                                splitLine: {show: false},
                                axisLine: {
                                    symbol: ['none', 'arrow'],
                                    lineStyle: {
                                        color: 'rgba(255,255,255,.6)',
                                        type: 'solid',
                                        opacity: 1
                                    }
                                },
                            },
                            {
                                type: 'value',
                                name: '增长率',
                                min: 0,
                                max: 25,
                                interval: 5,
                                axisLabel: {
                                    formatter: '{value} %',
                                    fontSize:14,
                                    color:'rgba(255,255,255,.6)',
                                },
                                splitLine: {show: false},
                                axisLine: {
                                    lineStyle: {
                                        color: 'rgba(255,255,255,.6)',
                                        type: 'solid',
                                        opacity: 1
                                    },
                                },
                            },
                        ],
                        series: [
                            {
                                name: '2月',
                                type: 'bar',
                                data: [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6],
                                tooltip: {
                                    valueFormatter: function (value) {
                                        return value + ' ml';
                                    },
                                },
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
                            },
                            {
                                name: '3月',
                                type: 'bar',
                                data: [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6],
                                tooltip: {
                                    valueFormatter: function (value) {
                                        return value + ' ml';
                                    }
                                },
                                itemStyle: {
                                    normal: {
                                        color: '#4695D1'
                                    },
                                },
                                markPoint: {
                                    data: [
                                        { type: 'max', name: 'Max' },
                                        { type: 'min', name: 'Min' }],
                                },
                            },
                            {
                                name: '增长率',
                                type: 'line',
                                yAxisIndex: 1,
                                data: [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3],
                                tooltip: {
                                    valueFormatter: function (value) {
                                        return value + ' °C';
                                    },
                                },
                                itemStyle: {
                                    normal: {
                                        color: '#6EB7BD'
                                    },
                                },
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

    // 中间第二个可视化图表
    function echarts_c2() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echarts-c2'));
        $.ajax({
            url: '/l2',
            success: function (data) {
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
                            right: '1%',                                   //图表距离容器右侧侧多少距离
                            bottom: '1%',                                  //图表距离容器上面多少距离
                            top: '15%',                                    //图表距离容器下面多少距离
                            containLabel: true,                            //防止标签溢出
                        },
                        legend: {
                            data: ['2月', '3月', '增长率'],
                            textStyle:{
                                color: 'rgba(255,255,255,.6)',
                                fontSize: 14,
                            }
                        },
                        xAxis: [
                            {
                                type: 'category',
                                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                                axisPointer: {
                                    type: 'shadow'
                                },
                                splitLine: {show: false},
                                axisLine: {
                                    symbol: ['none','arrow'],
                                    lineStyle: {
                                        color: 'rgba(255, 255, 255, .6)',
                                    }
                                },
                                axisLabel: {
                                    fontSize: 14,
                                    color: 'rgba(255, 255, 255, .6)'
                                }
                            }
                        ],
                        yAxis: [
                            {
                                type: 'value',
                                name: '浏览量',
                                min: 0,
                                max: 250,
                                interval: 50,
                                axisLabel: {
                                    formatter: '{value} ',
                                    fontSize:14,
                                    color:'rgba(255,255,255,.6)',
                                },
                                splitLine: {show: false},
                                axisLine: {
                                    symbol: ['none', 'arrow'],
                                    lineStyle: {
                                        color: 'rgba(255,255,255,.6)',
                                        type: 'solid',
                                        opacity: 1
                                    }
                                },
                            },
                            {
                                type: 'value',
                                name: '增长率',
                                min: 0,
                                max: 25,
                                interval: 5,
                                axisLabel: {
                                    formatter: '{value} %',
                                    fontSize:14,
                                    color:'rgba(255,255,255,.6)',
                                },
                                splitLine: {show: false},
                                axisLine: {
                                    lineStyle: {
                                        color: 'rgba(255,255,255,.6)',
                                        type: 'solid',
                                        opacity: 1
                                    },
                                },
                            },
                        ],
                        series: [
                            {
                                name: '2月',
                                type: 'bar',
                                data: [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6],
                                tooltip: {
                                    valueFormatter: function (value) {
                                        return value + ' ml';
                                    },
                                },
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
                            },
                            {
                                name: '3月',
                                type: 'bar',
                                data: [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6],
                                tooltip: {
                                    valueFormatter: function (value) {
                                        return value + ' ml';
                                    }
                                },
                                itemStyle: {
                                    normal: {
                                        color: '#4695D1'
                                    },
                                },
                                markPoint: {
                                    data: [
                                        { type: 'max', name: 'Max' },
                                        { type: 'min', name: 'Min' }],
                                },
                            },
                            {
                                name: '增长率',
                                type: 'line',
                                yAxisIndex: 1,
                                data: [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3],
                                tooltip: {
                                    valueFormatter: function (value) {
                                        return value + ' °C';
                                    },
                                },
                                itemStyle: {
                                    normal: {
                                        color: '#6EB7BD'
                                    },
                                },
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

    // 右边第一个可视化图表
    function echarts_r1() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echarts-r1'));
        $.ajax({
            url: '/month_flow_r1',
            success: function (data) {
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
                        right: '1%',                                   //图表距离容器右侧侧多少距离
                        bottom: '1%',                                  //图表距离容器上面多少距离
                        top: '15%',                                    //图表距离容器下面多少距离
                        containLabel: true,                            //防止标签溢出
                    },
                    legend: {
                        data: ['2月', '3月', '增长率'],
                        textStyle:{
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 14,
                        }
                    },
                    xAxis: [
                        {
                            type: 'category',
                            data: data["uv_day_index"],
                            axisPointer: {
                                type: 'shadow'
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none','arrow'],
                                lineStyle: {
                                    color: 'rgba(255, 255, 255, .6)',
                                }
                            },
                            axisLabel: {
                                fontSize: 14,
                                color: 'rgba(255, 255, 255, .6)'
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '浏览量(单位：k)',
                            scale: true,
                            axisLabel: {
                                formatter: '{value}',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none', 'arrow'],
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                }
                            },
                        },
                        {
                            type: 'value',
                            name: '增长率',
                            scale: true,
                            axisLabel: {
                                formatter: '{value} %',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                },
                            },
                        },
                    ],
                    series: [
                        {
                            name: '2月',
                            type: 'bar',
                            data: data["last_uv_day_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
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
                        },
                        {
                            name: '3月',
                            type: 'bar',
                            data: data["uv_day_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#4695D1'
                                },
                            },
                            markPoint: {
                                data: [
                                    { type: 'max', name: 'Max' },
                                    { type: 'min', name: 'Min' }],
                            },
                        },
                        {
                            name: '增长率',
                            type: 'line',
                            yAxisIndex: 1,
                            data: data["uv_day_rate"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + '%';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#6EB7BD'
                                },
                            },
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

    // 右边第二个可视化图表
    function echarts_r2() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echarts-r2'));
        $.ajax({
            url: '/month_flow_r2',
            success: function (data) {
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
                        right: '1%',                                   //图表距离容器右侧侧多少距离
                        bottom: '1%',                                  //图表距离容器上面多少距离
                        top: '15%',                                    //图表距离容器下面多少距离
                        containLabel: true,                            //防止标签溢出
                    },
                    legend: {
                        data: ['2月', '3月', '增长率'],
                        textStyle:{
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 14,
                        }
                    },
                    xAxis: [
                        {
                            type: 'category',
                            data: data["uv_hour_index"],
                            axisPointer: {
                                type: 'shadow'
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none','arrow'],
                                lineStyle: {
                                    color: 'rgba(255, 255, 255, .6)',
                                }
                            },
                            axisLabel: {
                                fontSize: 14,
                                color: 'rgba(255, 255, 255, .6)'
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '浏览量(单位：k)',
                            scale: true,
                            axisLabel: {
                                formatter: '{value}',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none', 'arrow'],
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                }
                            },
                        },
                        {
                            type: 'value',
                            name: '增长率',
                            scale: true,
                            axisLabel: {
                                formatter: '{value} %',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                },
                            },
                        },
                    ],
                    series: [
                        {
                            name: '2月',
                            type: 'bar',
                            data: data["last_uv_hour_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
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
                        },
                        {
                            name: '3月',
                            type: 'bar',
                            data: data["uv_hour_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#4695D1'
                                },
                            },
                            markPoint: {
                                data: [
                                    { type: 'max', name: 'Max' },
                                    { type: 'min', name: 'Min' }],
                            },
                        },
                        {
                            name: '增长率',
                            type: 'line',
                            yAxisIndex: 1,
                            data: data["uv_hour_rate"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + '%';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#6EB7BD'
                                },
                            },
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

    // 右边第三个可视化图表
    function echarts_r3() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echarts-r3'));
        $.ajax({
            url: '/month_flow_r3',
            success: function (data) {
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
                        right: '1%',                                   //图表距离容器右侧侧多少距离
                        bottom: '1%',                                  //图表距离容器上面多少距离
                        top: '15%',                                    //图表距离容器下面多少距离
                        containLabel: true,                            //防止标签溢出
                    },
                    legend: {
                        data: ['2月', '3月', '增长率'],
                        textStyle:{
                            color: 'rgba(255,255,255,.6)',
                            fontSize: 14,
                        }
                    },
                    xAxis: [
                        {
                            type: 'category',
                            data: data["uv_week_index"],
                            axisPointer: {
                                type: 'shadow'
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none','arrow'],
                                lineStyle: {
                                    color: 'rgba(255, 255, 255, .6)',
                                }
                            },
                            axisLabel: {
                                fontSize: 14,
                                color: 'rgba(255, 255, 255, .6)'
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '浏览量(单位：k)',
                            scale: true,
                            axisLabel: {
                                formatter: '{value}',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                symbol: ['none', 'arrow'],
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                }
                            },
                        },
                        {
                            type: 'value',
                            name: '增长率',
                            scale: true,
                            axisLabel: {
                                formatter: '{value} %',
                                fontSize:14,
                                color:'rgba(255,255,255,.6)',
                            },
                            splitLine: {show: false},
                            axisLine: {
                                lineStyle: {
                                    color: 'rgba(255,255,255,.6)',
                                    type: 'solid',
                                    opacity: 1
                                },
                            },
                        },
                    ],
                    series: [
                        {
                            name: '2月',
                            type: 'bar',
                            data: data["last_uv_week_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
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
                        },
                        {
                            name: '3月',
                            type: 'bar',
                            data: data["uv_week_value"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + 'k';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#4695D1'
                                },
                            },
                            markPoint: {
                                data: [
                                    { type: 'max', name: 'Max' },
                                    { type: 'min', name: 'Min' }],
                            },
                        },
                        {
                            name: '增长率',
                            type: 'line',
                            yAxisIndex: 1,
                            data: data["uv_week_rate"],
                            tooltip: {
                                valueFormatter: function (value) {
                                    return value + '%';
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: '#6EB7BD'
                                },
                            },
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

    // 中间总览第一个饼图
    function pe01() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('pe01'));
        var txt=81
        option = {
            title: {
              text: txt+'%',
              x: 'center',
             y: 'center',
              textStyle: {
                fontWeight: 'normal',
                color: '#fff',
                fontSize: '18'
              }
            },
            color:'rgba(255,255,255,.3)',
         
            series: [{
              name: 'Line 1',
              type: 'pie',
              clockWise: true,
              radius: ['65%', '80%'],
              itemStyle: {
                normal: {
                  label: {
                    show: false
                  },
                  labelLine: {
                    show: false
                  }
                }
              },
              hoverAnimation: false,
              data: [{
                value: txt,
                name: '已使用',
                itemStyle: {
                  normal: {
                    color:'#eaff00',
                    label: {
                      show: false
                    },
                    labelLine: {
                      show: false
                    }
                  }
                }
              }, {
                name: '未使用',
                value: 100-txt
              }]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }

    // 中间总览第二个饼图
    function pe02() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('pe02'));
        var txt=17
        option = {
            title: {
              text: txt+'%',
              x: 'center',
             y: 'center',
              textStyle: {
                fontWeight: 'normal',
                color: '#fff',
                fontSize: '18'
              }
            },
            color:'rgba(255,255,255,.3)',
         
            series: [{
              name: 'Line 1',
              type: 'pie',
              clockWise: true,
              radius: ['65%', '80%'],
              itemStyle: {
                normal: {
                  label: {
                    show: false
                  },
                  labelLine: {
                    show: false
                  }
                }
              },
              hoverAnimation: false,
              data: [{
                value: txt,
                name: '已使用',
                itemStyle: {
                  normal: {
                    color:'#ea4d4d',
                    label: {
                      show: false
                    },
                    labelLine: {
                      show: false
                    }
                  }
                }
              }, {
                name: '未使用',
                value: 100-txt
              }]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }

    // 中间总览第三个饼图
    function pe03() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('pe03'));
        var txt=2
        option = {
            title: {
              text: txt+'%',
              x: 'center',
             y: 'center',
              textStyle: {
                fontWeight: 'normal',
                color: '#fff',
                fontSize: '18'
              }
            },
            color:'rgba(255,255,255,.3)',
         
            series: [{
              name: 'Line 1',
              type: 'pie',
              clockWise: true,
              radius: ['65%', '80%'],
              itemStyle: {
                normal: {
                  label: {
                    show: false
                  },
                  labelLine: {
                    show: false
                  }
                }
              },
              hoverAnimation: false,
              data: [{
                value: txt,
                name: '已使用',
                itemStyle: {
                  normal: {
                    color:'#395ee6',
                    label: {
                      show: false
                    },
                    labelLine: {
                      show: false
                    }
                  }
                }
              }, {
                name: '未使用',
                value: 100-txt
              }
            ]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
})



		
		
		


		



















