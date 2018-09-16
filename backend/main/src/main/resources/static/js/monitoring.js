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
        setResults();
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
    if (padding == 0) padding = 1000;
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

function setResults() {
    if (mon.results == undefined) return;
    document.getElementById('results-controls').style.display = 'block';
    var len = mon.results.length;
    var selector = document.getElementById('inputResultsDate');
    selector.innerHTML = '';
    for (var i = 0; i < len; i++) {
        var item = mon.results[i];
        var date = new Date(item.time * 1000);
        var time = date.getDate().pad(2) + '.' + (date.getMonth()+1).pad(2) + ', ' + date.getHours().pad(2) + ':' + date.getMinutes().pad(2);
        var str = '<option name="res-' + i + '">' + time + '</option>';
        selector.innerHTML = selector.innerHTML + str;
    }
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

function showResults() {
    document.getElementById('search-label').style.display = 'none';
    var container = document.getElementById('results-container');
    var selected = parseInt($('#inputResultsDate').find(":selected").attr('name').substr(4));
    var block = mon.results[selected]['results'];
    var len = block.length;
    container.innerHTML = '';
    for (var i = 0; i < len; i++) {
        container.innerHTML += generateListItem(block[i]);
    }
    if (len == 0) {
        document.getElementById('search-label').style.display = 'inline-block';
    }
}

function generateListItem(tour) {
    var hotel_photo_url = tour.hotel.images.length > 0 ? tour.hotel.images[0] : "";
    var location = tour.country;
    var date = tour.date_start.substring(8, 10) + '.' + tour.date_start.substring(5, 7);
    var nights;
    if (tour.nights == 1) nights = ' ночь';
    else if (tour.nights >= 2 && tour.nights <= 4) nights = ' ночи';
    else nights = ' ночей';
    nights = tour.nights + nights;
    var meals = getMealName(tour.meals);


    var s = '<div class="card flex-row flex-wrap" style="margin-top: 20px;">';
    s += '<div style="width: 300px; height: 200px;">';
    s += '<div class="border-0">';
    s += '<img class="tour-image" src="' + hotel_photo_url + '" alt="">';
    s += '</div>';
    s += '</div>';
    s += '<div class="card-block px-2 tour-content">';
    s += '<a href="' + tour.hotel.url + '" class="tour-description-item tour-header">' + tour.hotel.name + '</a>';
    s += '<div class="tour-place">' + location + '</div>';
    s += '<div class="tour-description-item">';
    s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24"> <path fill="#000000" d="M7,10H12V15H7M19,19H5V8H19M19,3H18V1H16V3H8V1H6V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3Z" /> </svg>';
    s += '<span class="tour-description-item-text">' + date + '</span>';
    s += '</div>';
    s += '<div class="tour-description-item">';
    s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24"> <path fill="#000000" d="M17.75,4.09L15.22,6.03L16.13,9.09L13.5,7.28L10.87,9.09L11.78,6.03L9.25,4.09L12.44,4L13.5,1L14.56,4L17.75,4.09M21.25,11L19.61,12.25L20.2,14.23L18.5,13.06L16.8,14.23L17.39,12.25L15.75,11L17.81,10.95L18.5,9L19.19,10.95L21.25,11M18.97,15.95C19.8,15.87 20.69,17.05 20.16,17.8C19.84,18.25 19.5,18.67 19.08,19.07C15.17,23 8.84,23 4.94,19.07C1.03,15.17 1.03,8.83 4.94,4.93C5.34,4.53 5.76,4.17 6.21,3.85C6.96,3.32 8.14,4.21 8.06,5.04C7.79,7.9 8.75,10.87 10.95,13.06C13.14,15.26 16.1,16.22 18.97,15.95M17.33,17.97C14.5,17.81 11.7,16.64 9.53,14.5C7.36,12.31 6.2,9.5 6.04,6.68C3.23,9.82 3.34,14.64 6.35,17.66C9.37,20.67 14.19,20.78 17.33,17.97Z" /> </svg>';
    s += '<span class="tour-description-item-text">' + nights + '</span>';
    s += '</div>';
    s += '<div class="tour-description-item">';
    s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24"> <path fill="#000000" d="M11,9H9V2H7V9H5V2H3V9C3,11.12 4.66,12.84 6.75,12.97V22H9.25V12.97C11.34,12.84 13,11.12 13,9V2H11V9M16,6V14H18.5V22H21V2C18.24,2 16,4.24 16,6Z" /> </svg>';
    s += '<span class="tour-description-item-text">' + meals + '</span>';
    s += '</div>';
    s += '</div>';
    s += '<div class="w-100"></div>';
    s += '<div class="align-middle card-footer w-100 text-muted">';
    s += '<a href="' + tour.booking_url + '" class="btn btn-dark" target="_blank" style="float: right;">Бронировать</a>';
    s += '<h6 class="price-tag">' + parseInt(tour.price) + ' грн</h6>';
    s += '</div>';
    s += '</div>';
    return s;
}