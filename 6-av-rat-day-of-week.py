import justpy as jp
import pandas
from datetime import datetime
from pytz import utc

data = pandas.read_csv("data/reviews/reviews.csv", parse_dates=["Timestamp"])
data['Weekday'] = data['Timestamp'].dt.strftime("%A")
data['Daynumber'] = data['Timestamp'].dt.strftime("%w")
weekday_average = data.groupby(['Weekday', "Daynumber"]).mean()
weekday_average = weekday_average.sort_values("Daynumber")

chart_def = """
 {
    chart: {
        type: 'spline',
        inverted: false
    },
    title: {
        text: 'Atmosphere Temperature by Altitude'
    },
    subtitle: {
        text: 'According to the Standard Atmosphere Model'
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Date'
        },
        labels: {
            format: '{value}'
        },
        
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Rating'
        },
        labels: {
            format: '{value}°'
        },
      
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.x}: {point.y}'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Avg. Rating',
     
    }]
}
"""


def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp, text="Analysis of Course Reviews",
                 classes="text-h3 text-center q-pa-md")
    p1 = jp.QDiv(a=wp, text="These graphs represent course review analysis")
    hc = jp.HighCharts(a=wp, options=chart_def)
    hc.options.title.text = "Average Rating by Day"
    hc.options.xAxis.categories = list(weekday_average.index)
    hc.options.series[0].data = list(weekday_average["Rating"])
    return wp


jp.justpy(app)
