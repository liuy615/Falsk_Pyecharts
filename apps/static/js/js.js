$(window).load(function(){$(".loading").fadeOut()})
$(function () {

    echarts_2()
    echarts_3()
    echarts_4()
    echarts_5()
    echarts_6()

    function echarts_2() {
            // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart2'));
        $.ajax({
            url: "l2",
            success:function (data) {
                option = {
                    grid: {
                        left: '0',
                        top:'0',
                        right: '0',
                        bottom: '0%',
                       containLabel: true
                    },
                    xAxis: {
                        show: false
                    },
                    yAxis: [{
                        show: true,
                        data: data["类型"],
                        inverse: true,
                        axisLine: { show: false},
                        splitLine:{ show: false},
                        axisTick:{ show: false},
                        axisLabel: {
                            textStyle: {
                                color:'#fff'
                            },
                        },
                    }],
                    series: [{
                        name: '条',
                        type: 'bar',
                        yAxisIndex: 0,
                        data: data["数量"],
                        barWidth: 15,
                        itemStyle: {
                            normal: {
                               barBorderRadius: 50,
                                color:'#1089E7',
                            }
                        },
                        label: {
                           normal: {
                                show: true,
                                position: 'right',
                                formatter: '{c}',
                               textStyle: {color: 'rgba(255,255,255,.5)'}
                            }
                        },
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


    // echarts_3是中间第二个可视化图表
    function echarts_3() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart3'));
        $.ajax({
            url:"/c2",
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

    // echatrs_4是右边第一个图
    function echarts_4() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart4'));
        $.ajax({
            url: "/r1",
            success: function (data) {
                option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        },
                        formatter: function (params) {
                            var tar = params[1];
                            return tar.name + '<br/>' + tar.seriesName + ' : ' + tar.value;
                        }
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        top:'3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'category',
                        splitLine: { show: false },
                        data: data["city_level"]
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            name: 'Placeholder',
                            type: 'bar',
                            stack: 'Total',
                            itemStyle: {
                                borderColor: 'transparent',
                                color: 'transparent'
                            },
                            emphasis: {
                                itemStyle: {
                                    borderColor: 'transparent',
                                    color: 'transparent'
                                }
                            },
                            data: data["city_none"]
                        },
                        {
                            name: '会员人数',
                            type: 'bar',
                            stack: 'Total',
                            label: {
                                show: true,
                                position: 'inside'
                            },
                            data: data["data_city_level"]
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

    // echatrs_5 是右边第二个图：会员性别分布图
    function echarts_5() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart5'));
        $.ajax({
            url:"/r2",
            success: function (data) {
                option = {
                    tooltip: {
                        trigger: 'item'
                    },
                    legend: {
                        top: '5%',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: '{a} <br/>{b} : {c} ({d}%)'
                    },
                    series: [
                        {
                            name: '会员性别分布',
                            type: 'pie',
                            radius: ['40%', '70%'],
                            avoidLabelOverlap: false,
                            itemStyle: {
                                borderRadius: 10,
                                borderColor: '#3893e5',
                                borderWidth: 2
                            },
                            label: {
                                show: false,
                                position: 'center'
                            },
                            emphasis: {
                                label: {
                                    show: true,
                                    fontSize: 40,
                                    fontWeight: 'bold'
                                }
                            },
                            labelLine: {
                                show: false
                            },
                            data: [
                                { value: data["1"], name: '男' },
                                { value: data["0"], name: '女' },
                                { value: data["-1"], name: '未知' },
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

    // echarts_6 是右边第三个图
    function echarts_6() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart6'));
        $.ajax({
            url:"/r3",
            success: function (data) {
                option = {
                    tooltip: {
                        trigger: 'axis'
                    },
                    radar: [{
                        indicator: [
                            {text: '一级', max: 330000},
                            {text: '二级', max: 330000},
                            {text: '三级', max: 330000},
                            {text: '四级', max: 330000},
                            {text: '五级', max: 330000},
                            {text: '六级', max: 330000},
                            {text: '七级', max: 330000},
                        ],
                        textStyle: {
                            color: 'red'
                        },
                        center: ['50%', '50%'],
                        radius: '70%',
                        startAngle: 90,
                        splitNumber: 4,
                        shape: 'circle',
                        name: {
                            padding:-5,
                            formatter: '{value}',
                            textStyle: {
                                color: 'rgba(255,255,255,.5)'
                            }
                        },
                        splitArea: {
                            areaStyle: {
                                color: 'rgba(255,255,255,.05)'
                            }
                        },
                        axisLine: {
                            lineStyle: {
                                color: 'rgba(255,255,255,.05)'
                            }
                        },
                        splitLine: {
                            lineStyle: {
                                color: 'rgba(255,255,255,.05)'
                            }
                        }
                    }],
                    series: [{
                        name: '雷达图',
                        type: 'radar',
                        tooltip: {
                            trigger: 'item'
                        },
                        data: [
                        {
                            name: '会员等级',
                            value: data["num"],
                            symbolSize: 0,
                            lineStyle: {
                                normal: {
                                    color:'#3893e5',
                                    width:2,
                                }
                            },
                            areaStyle: {
                                normal: {
                                    color: 'rgba(19, 173, 255, 0.5)'
                                }
                            }
                        }]
                    }]
                };
                myChart.setOption(option);
                window.addEventListener("resize",function(){
                    myChart.resize();
                });
            }
        })
    }
})



		
		
		


		









