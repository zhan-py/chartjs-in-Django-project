var bgColorGreen = 'rgba(96, 150, 220, 0.5)';
var colorGreen = 'rgba(96, 150, 220, 1)';

var bgColorRed = 'rgba(254, 213, 86, 0.5)';
var colorRed = 'rgba(254, 213, 86, 1)';

    const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    //line chart
    var chartData = {
        "labels": [2020, 2021, 2022, 2023],
        "data_set": [30000.0, 50000.0, 79000.0, 90000.0]
    };

    var ctx = document.getElementById('myChart').getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Donation by Year',
                data: chartData.data_set,
                borderColor: colorGreen,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
              title: {
                display: true,
                text: 'Donation Trends Over the Years',
              },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value, index, values) {
                            return value / 1000 + 'K';
                        }
                    }
                }
            }
        }
    });


    // column chart
    var colmunChartData = {
        "labels": ["AC", "BBW", "BF", "BRF", "CBOQ", "JE", "LG", "MH", "OTH", "OWEC", "PIM", "WG"], 
        "data_current_year": [15000.0, 11000.0, 8000.0, 9000.0, 1000.0, 8000.0, 9000.0, 7000.0, 10000.0, 4000.0, 3000.0, 5000.0], 
        "data_previous_year": [7000.0, 4000.0, 6000.0, 11000.0, 7000.0, 9000.0, 5000.0, 8000.0, 6000.0, 6000.0, 5000.0, 5000.0]
    }

    var ctx1 = document.getElementById('colmunChart').getContext('2d');

    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: colmunChartData.labels,
            datasets: [{
                label: 'Current Year',
                data: colmunChartData.data_current_year,
                backgroundColor: bgColorGreen,
                borderColor: colorGreen,
                borderWidth: 1
              },
              {
                label: 'Previous Year',
                data: colmunChartData.data_previous_year,
                backgroundColor: bgColorRed,
                borderColor: colorRed,
                borderWidth: 1
              }
            ]
        },
        options: {
            plugins: {
                title: {
                  display: true,
                  text: 'Donation Amount by Category',
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                }
            }
        }
    });


    // double column chart
    var colmunChartData = {
        "labels": MONTHS, 
        "data_current_year": [1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2], 
        "data_last_year": [1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2]
    }

    var ctx2 = document.getElementById('doubleColmunChart').getContext('2d');

    new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: colmunChartData.labels,
            datasets: [{
            label: 'Current Year',
            data: colmunChartData.data_current_year,
            backgroundColor: bgColorGreen,
            borderColor: colorGreen,
            borderWidth: 1,
        }, {
            label: 'Previous Year',
            data: colmunChartData.data_last_year,
            backgroundColor: bgColorRed,
            borderColor: colorRed,
            borderWidth: 1,
        }]
        },
        options: {
            plugins: {
                  title: {
                    display: true,
                    text: 'Comparison of Current and Previous Year Donation Count',
                  },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0,
                    }
                }
            },
            barPercentage: 0.95, 
            categoryPercentage: 0.7, 
        }
    });


    //area line chart
    var areaChartData = {
        "labels": MONTHS, 
        "data_series1": [8000.0, 7000.0, 7000.0, 5000.0, 11000.0, 9000.0, 8000.0, 10000.0, 7000.0, 5000.0, 13000.0], 
        "data_series2": [5000.0, 6000.0, 7000.0, 6000.0, 5000.0, 7000.0, 5000.0, 10000.0, 9000.0, 6000.0, 4000.0, 9000.0]
    }

    var ctx3 = document.getElementById('areaChart').getContext('2d');
    new Chart(ctx3, {
        type: 'line',
        data: {
            labels: areaChartData.labels,
            datasets: [{
                label: 'Current Year',
                data: areaChartData.data_series1,
                fill: true, 
                backgroundColor: bgColorGreen,
                borderColor: colorGreen,
                borderWidth: 1
            }, {
                label: 'Previous Year',
                data: areaChartData.data_series2,
                fill: true, 
                backgroundColor: bgColorRed,
                borderColor: colorRed,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title: {
                  display: true,
                  text: 'Comparison of Current and Previous Year Donation Amount',
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                },
                x: {
                    grid: {
                          // display: false,
                    },
                }
            }
        }
    });

