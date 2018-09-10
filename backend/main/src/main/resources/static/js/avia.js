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
        "startDate": moment().add(3, 'days'),
        "endDate": moment().add(6, 'days'),
        "minDate": moment()
    }, function(start, end, label) {
        minDate = start.format('YYYYMMDD');
        maxDate = end.format('YYYYMMDD');
        console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
    });
}

function restrictMaxNightsInput() {
    var value = parseInt(document.getElementById("minNights").value);
    var inp = document.getElementById("maxNights");
    inp.min = value;
    inp.max = value + 8;
    if (parseInt(inp.value) < value) inp.value = value;
}

function test() {
    $.ajax({
        url: "http://localhost:8080/api/tours/avia?meals=ai&adults=2&children=1&start_date_from=20180917&start_date_to=20180918&nights_min=6&nights_max=10&price_max=39990&code_country=eg"
    }).then(function(data) {
        // obj.hasOwnProperty('field')
        var len = data.data.length;
        for (var i = 0; i < len; i++) {
            $('#tours-container').append(generateListItem(data.data[i]));
        }
    });
}

function loadTours() {
    if (minDate == undefined) minDate = moment().add(3, 'days').format('YYYYMMDD');
    if (maxDate == undefined) maxDate = moment().add(6, 'days').format('YYYYMMDD');
    var minNights = document.getElementById('minNights').value;
    var maxNights = document.getElementById('maxNights').value;
    var country = $('#inputCountry').find(":selected").attr('name').substr(8);
    var adults = parseInt($('#inputAdults').find(":selected").text());
    var children = $('#inputChildren').find(":selected").text();
    var meals = $('#inputMeals').find(":selected").attr('name').substr(5);
    var maxPrice = document.getElementById('inputMaxPrice').value;

    var requestUrl = 'http://localhost:8080/api/tours/avia?';
    requestUrl += 'meals=' + meals + '&adults=' + adults + '&children=' + children + '&code_country=' + country;
    requestUrl += '&start_date_from=' + minDate + '&start_date_to=' + maxDate + '&price_max=' + maxPrice;
    requestUrl += '&nights_min=' + minNights + '&nights_max=' + maxNights;

    document.getElementById('search-button').class = "btn disabled";
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
        s += '<a href="' + tour.booking_url + '" class="btn btn-dark" style="float: right;">Бронировать</a>';
        s += '<h6 class="price-tag">' + parseInt(tour.price) + ' грн</h6>';
    s += '</div>';
    s += '</div>';
    return s;
}