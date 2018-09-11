function init() {
    init_calendar();
}

var minDate, maxDate;
function init_calendar() {
    $('input[name="date_range"]').daterangepicker({
        "locale": {
            "format": "DD.MM.YYYY",
            "separator": " - ",
            "applyLabel": "Выбрать",
            "cancelLabel": "Отмена",
            "fromLabel": "С",
            "toLabel": "По",
            "customRangeLabel": "Custom",
            "weekLabel": "W",
            "daysOfWeek": [
                "Вс",
                "Пн",
                "Вт",
                "Ср",
                "Чт",
                "Пт",
                "Сб"
            ],
            "monthNames": [
                "Январь",
                "Февраль",
                "Март",
                "Апрель",
                "Май",
                "Июнь",
                "Июль",
                "Август",
                "Сентябрь",
                "Октябрь",
                "Ноябрь",
                "Декабрь"
            ],
            "firstDay": 1
        },
        "startDate": moment().add(10, 'days'),
        "endDate": moment().add(30, 'days'),
        "minDate": moment()
    }, function(start, end, label) {
        minDate = start.format('YYYYMMDD');
        maxDate = end.format('YYYYMMDD');
        console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
    });
}

function loadTours() {
    if (minDate == undefined) minDate = moment().add(10, 'days').format('YYYYMMDD');
    if (maxDate == undefined) maxDate = moment().add(30, 'days').format('YYYYMMDD');
    var minDays = document.getElementById('minDays').value;
    var maxDays = document.getElementById('maxDays').value;
    var places = document.getElementById('inputPlaces').value;
    var places_mode = document.getElementById('placesRadio1').checked == true ? 'all' : 'one';
    var maxPrice = document.getElementById('inputMaxPrice').value;

    var requestUrl = 'http://localhost:8080/api/tours/bus?';
    requestUrl += 'places_str=' + places + '&places_mode=' + places_mode;
    requestUrl += '&start_date_from=' + minDate + '&start_date_to=' + maxDate + '&price_max=' + maxPrice;
    requestUrl += '&days_min=' + minDays + '&days_max=' + maxDays;

    document.getElementById('search-label').style.display = 'block';
    $.ajax({
        url: requestUrl
    }).then(function(data) {
        // obj.hasOwnProperty('field')
        document.getElementById('tours-container').innerHTML = '';
        document.getElementById('search-label').style.display = 'none';
        var len = data.data.length;
        for (var i = 0; i < len; i++) {
            $('#tours-container').append(generateListItem(data.data[i]));
        }
    });
}

function getPriceString(price, currency) {
    if (currency == 'UAH') return 'от ' + price + ' грн';
    if (currency == 'EUR') return 'от ' + price + ' €';
    return 'от ' + price + ' ' + currency;
}

function generateListItem(tour) {
    var photo_url = tour.image;
    var route = tour.route_str;
    var days;
    if (tour.days == 1) days = ' день';
    else if (tour.days >= 2 && tour.days <= 4) days = ' дня';
    else days = ' дней';
    days = tour.days + days;
    var price = getPriceString(tour.price, tour.currency);

    var s = '<div class="card flex-row flex-wrap" style="margin-top: 20px;">';
    s += '<div style="width: 300px; height: 200px;">';
    s += '<div class="border-0">';
        s += '<img class="tour-image" src="' + photo_url + '" alt="">';
    s += '</div>';
    s += '</div>';
    s += '<div class="card-block px-2 tour-content">';
        s += '<a href="' + tour.url + '" class="tour-description-item tour-header">' + tour.title + '</a>';
    s += '<div class="tour-place">' + route + '</div>';
    s += '<div class="tour-description-item">';
        s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24"> <path fill="#000000" d="M7,10H12V15H7M19,19H5V8H19M19,3H18V1H16V3H8V1H6V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3Z" /> </svg>';
        s += '<span class="tour-description-item-text">' + days + '</span>';
    s += '</div>';
    s += '</div>';
    s += '<div class="w-100"></div>';
        s += '<div class="align-middle card-footer w-100 text-muted">';
        s += '<a href="' + tour.url + '" class="btn btn-dark" style="float: right;">Подробнее</a>';
        s += '<h6 class="price-tag">' + price + '</h6>';
    s += '</div>';
    s += '</div>';
    return s;
}