// JS 代码
// var counts = {{ res | safe }}

Highcharts.chart('pie_container', {
    chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
    },
    credits: {
        enabled: false
    },
    title: {
            text: '手机评价所占比例'
    },
    tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
            pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                            style: {
                                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                            }
                    }
            }
    },
    series: [{
            name: 'Brands',
            colorByPoint: true,
            data: counts
    }]
});
