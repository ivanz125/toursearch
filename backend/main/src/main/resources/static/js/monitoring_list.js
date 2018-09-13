function init() {
    loadMonitorings();
}

function loadMonitorings() {
    userId = document.getElementById('userId').value;

    var requestUrl = 'http://localhost:8080/api/monitoring/get?user_id=' + 1;
    $.ajax({
        url: requestUrl
    }).then(function(data) {
        // obj.hasOwnProperty('field')
        document.getElementById('tours-container').innerHTML = '';
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

function generateListItem(monitoring) {
    var date1 = (monitoring.params.start_date_from + '').substring(6, 8)
        + '.' + (monitoring.params.start_date_from + '').substring(4, 6);
    var date2 = (monitoring.params.start_date_to + '').substring(6, 8)
        + '.' + (monitoring.params.start_date_to + '').substring(4, 6);
    var date = date1 == date2 ? date1 : date1 + ' - ' + date2;
    var n1 = monitoring.params.nights_min;
    var n2 = monitoring.params.nights_max;
    var nights;
    if (n2 == 1) nights = ' ночь';
    else if (n2 >= 2 && n2 <= 4) nights = ' ночи';
    else nights = ' ночей';
    nights = n1 == n2 ? n1 + nights : n1 + ' - ' + n2 + nights;
    var meals = getMealName(monitoring.params.meals);
    var priceLimit = 'до ' + monitoring.params.price_limit + ' грн';


    var s = '<div class="card flex-row flex-wrap" style="margin-top: 20px;">';
    s += '<div class="card-block px-2 tour-content" style="padding-bottom: 12px;">';
        s += '<a href="/monitoring?id=' + parseInt(monitoring.id) + '" class="tour-description-item tour-header">' + monitoring.name + '</a>';
    s += '<div class="tour-place">' + monitoring.country + '</div>';
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
    s += '<div class="tour-description-item">';
        s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24"><path fill="#000000" d="M7,15H9C9,16.08 10.37,17 12,17C13.63,17 15,16.08 15,15C15,13.9 13.96,13.5 11.76,12.97C9.64,12.44 7,11.78 7,9C7,7.21 8.47,5.69 10.5,5.18V3H13.5V5.18C15.53,5.69 17,7.21 17,9H15C15,7.92 13.63,7 12,7C10.37,7 9,7.92 9,9C9,10.1 10.04,10.5 12.24,11.03C14.36,11.56 17,12.22 17,15C17,16.79 15.53,18.31 13.5,18.82V21H10.5V18.82C8.47,18.31 7,16.79 7,15Z" /> </svg>';
        s += '<span class="tour-description-item-text">' + priceLimit + '</span>';
    s += '</div>';
    s += '</div>';
    s += '<div class="w-100"></div>';
        s += '<div class="align-middle card-footer w-100 text-muted">';
        s += '<a href="#" class="btn btn-danger">Отключить</a>';
        s += '<a href="#" class="btn btn-dark" style="float: right;">Подробности</a>';
    s += '</div>';
    s += '</div>';
    return s;
}