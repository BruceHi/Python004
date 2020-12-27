// JS 代码

var chart = Highcharts.chart('bar_container',{
    // 第一字段，去掉版权信息
    credits: {
        enabled: false
    },
    chart: {
        type: 'column'
    },
    title: {
        text: '手机评价分布'
    },
    subtitle: {
        text: '数据来源: SMZDM.com'
    },
    xAxis: {
        categories: rates.phone_name,
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: '评价数量'
        }
    },
    tooltip: {
        // head + 每个 point + footer 拼接成完整的 table
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y:.1f} 个</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            // stacking: 'percent'
            borderWidth: 0
        }
    },
    series: [{
        name: '差评',
        data: rates.bad
    }, {
        name: '中评',
        data: rates.normal
    }, {
        name: '好评',
        data: rates.good
    }]
});