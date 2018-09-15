var mon;

function init() {
    loadMonitoring();
}

function loadMonitoring() {
    var monitoringId = document.getElementById('monitoringId').value;

    var requestUrl = 'http://localhost:8080/api/monitoring/get_one?id=' + monitoringId;
    $.ajax({
        url: requestUrl
    }).then(function(monitoring) {
        mon = monitoring;
        setMonitoring(monitoring);
        document.getElementById('tours-container').style.display = 'block';
        console.log(monitoring.results);
        chart(monitoring.results);
    }).catch(function(data) {
        alert('Ошибка. Обновите страницу.');
    });
}

function getMealName(meal) {
    switch (meal.toLowerCase()) {
        case 'ro':
            return 'Без питания';
        case 'bb':
            return 'Только завтрак';
        case 'hb':
            return 'Завтрак и ужин';
        case 'fb':
            return 'Завтрак, обед и ужин';
        case 'ai':
            return 'Все включено';
        case 'uai':
            return 'Ультра все включено';
        default:
            return 'Другое';
    }
}

function setMonitoring(monitoring) {
    var date1 = (monitoring.params.start_date_from + '').substring(6, 8)
        + '.' + (monitoring.params.start_date_from + '').substring(4, 6);
    var date2 = (monitoring.params.start_date_to + '').substring(6, 8)
        + '.' + (monitoring.params.start_date_to + '').substring(4, 6);
    var date = date1 == date2 ? date1 : date1 + ' - ' + date2;
    var people = monitoring.params.adults;
    if (people == 1) people = '1 взрослый';
    else people += ' взрослых';
    if (monitoring.params.children == 1) people += ', 1 ребенок';
    else if (monitoring.params.children == 2) people += ', 2 детей';
    var n1 = monitoring.params.nights_min;
    var n2 = monitoring.params.nights_max;
    var nights;
    if (n2 == 1) nights = ' ночь';
    else if (n2 >= 2 && n2 <= 4) nights = ' ночи';
    else nights = ' ночей';
    nights = n1 == n2 ? n1 + nights : n1 + ' - ' + n2 + nights;
    var meals = getMealName(monitoring.params.meals);
    var priceLimit = 'до ' + monitoring.params.price_limit + ' грн';
    // Buttons
    var active_button = '<span id="active_button" class="btn btn-danger" onclick="active()">Отключить</span>';
    if (monitoring.active == false) active_button
        = '<span id="active_button" class="btn btn-success" onclick="active()">Включить</span>';

    document.getElementById('monitoringName').innerHTML = monitoring.name;
    document.getElementById('monitoringCountry').innerHTML = monitoring.country;
    document.getElementById('monitoringDates').innerHTML = date;
    document.getElementById('monitoringPeople').innerHTML = people;
    document.getElementById('monitoringNights').innerHTML = nights;
    document.getElementById('monitoringMeals').innerHTML = meals;
    document.getElementById('monitoringPrice').innerHTML = priceLimit;
    document.getElementById('activeButtonContainer').innerHTML = active_button;
}

function chart(data) {
    var len = data.length;
    if (len == 0) {
        document.getElementById('priceChart').style.display = 'none';
        return;
    }
    var newData = [];
    var minPrice = 100000, maxPrice = 0;
    for (var i = 0; i < len; i++) {
        //var item = {"time": data[i].time, "tours": data[i].results_count};
        var date = new Date(data[i].time * 1000);
        var time = date.getDate().pad(2) + '.' + (date.getMonth()+1).pad(2) + ', ' + date.getHours().pad(2) + ':' + date.getMinutes().pad(2);
        var item = {"time": time, "price": data[i].min_price};
        minPrice = Math.min(data[i].min_price, minPrice);
        maxPrice = Math.max(data[i].min_price, maxPrice);
        newData.push(item);
    }
    var padding = (maxPrice - minPrice) / 8;
    var bottom = Math.round((minPrice - padding) / 100) * 100;
    var top = Math.round((maxPrice + padding) / 100) * 100;
    var interval = (top - bottom) / 10;
    console.log(newData);
    console.log(minPrice + ' ' + maxPrice);

    // prepare jqxChart settings
    var settings = {
        title: "Минимальная цена",
        description: "График минимальной цены на туры с заданными параметрами от времени",
        padding: { left: 5, top: 5, right: 50, bottom: 5 },
        titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
        source: newData,
        categoryAxis:
            {
                dataField: 'time',
                description: 'Время',
                displayField: 'Время',
                showGridLines: false
            },
        colorScheme: 'scheme01',
        seriesGroups:
            [
                {
                    type: 'line',
                    columnsGapPercent: 30,
                    seriesGapPercent: 0,
                    valueAxis:
                        {
                            minValue: bottom,
                            maxValue: top,
                            unitInterval: interval,
                            description: 'Минимальная цена'
                        },
                    series: [
                        { dataField: 'price', displayText: 'Минимальная цена тура'}
                    ]
                }
            ]
    };

    // select the chartContainer DIV element and render the chart.
    $('#priceChart').jqxChart(settings);
}

Number.prototype.pad = function(size) {
    var s = String(this);
    while (s.length < (size || 2)) {s = "0" + s;}
    return s;
};

function active() {
    var monitoringId = document.getElementById('monitoringId').value;
    //var active = document.getElementById('active_button').innerHTML != 'Отключить';
    var active = !mon.active;

    document.getElementById('activeButtonLabel').style.display = 'inline-block';
    var requestUrl = 'http://localhost:8080/api/monitoring/set_active?id=' + monitoringId + '&active=' + active;
    $.ajax({
        url: requestUrl
    }).then(function(data) {
        document.getElementById('active_button').innerHTML = active ? 'Отключить' : 'Включить';
        document.getElementById('active_button').class = active ? 'btn btn-danger' : 'btn btn-success';
        document.getElementById('activeButtonLabel').style.display = 'none';
        mon.active = active;
    }).catch(function(data) {
        console.log(data);
        document.getElementById('activeButtonLabel').innerHTML = 'Ошибка';
        setTimeout(function(){
            document.getElementById('activeButtonLabel').style.display = 'none';
            document.getElementById('activeButtonLabel').innerHTML = 'Переключение...';
        }, 2000);
        document.getElementById('active_button').innerHTML = active ? 'Включить' : 'Отключить';
        document.getElementById('active_button').class = active ? 'btn btn-success' : 'btn btn-danger';
    });
}

function remove() {
    var monitoringId = document.getElementById('monitoringId').value;

    document.getElementById('activeButtonLabel').style.display = 'inline-block';
    document.getElementById('activeButtonLabel').innerHTML = 'Удаление...';
    var requestUrl = 'http://localhost:8080/api/monitoring/delete?id=' + monitoringId;
    $.ajax({
        url: requestUrl,
        method: 'DELETE'
    }).then(function(data) {
        document.getElementById('activeButtonLabel').style.display = 'none';
        document.getElementById('activeButtonLabel').innerHTML = 'Переключение...';
        window.location.replace("/monitoring_list");
    }).catch(function(data) {
        console.log(data);
        document.getElementById('activeButtonLabel').innerHTML = 'Ошибка';
        setTimeout(function(){
            document.getElementById('activeButtonLabel').style.display = 'none';
            document.getElementById('activeButtonLabel').innerHTML = 'Переключение...';
        }, 2000);
    });
}