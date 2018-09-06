import requests


def convert_meal(name):
    if name == 'All Inclusive':
        return 'AI'
    elif name == 'Bed And Breakfast':
        return 'BB'
    elif name == 'Full Board':
        return 'FB'
    elif name == 'Half Board':
        return 'HB'
    elif name == 'Room Only':
        return 'RO'
    return name


def id_country_for_tui(code):
    if code == 'tr':
        return -18803
    if code == 'eg':
        return -18498
    return 0


def meals_for_tui(meals):
    if meals == 'ai':
        return 10004
    elif meals == 'bb':
        return 10001
    elif meals == 'fb':
        return 10003
    elif meals == 'hb':
        return 10002
    elif meals == 'ro':
        return 10005
    return 0


def get_results(code_country, start_date_from, start_date_to, adults, children, nights_min, nights_max, meals, price_max=0):
    params = {'adult':adults, 'checkinBegin':start_date_from, 'checkinEnd':start_date_to,
              'child':children, 'currency':4, 'groupByHotel':True,
              'isRuSite':False, 'nightMax':nights_max, 'nightMin':nights_min,
              'state':id_country_for_tui(code_country), 'townFrom':235144, 'meal':meals_for_tui(meals)}

    if price_max > 0:
        params['costMax'] = price_max
    print(params)
    resp = requests.get('http://www.tui.ua/api-agency/search/PriceList', params=params)

    tours_json = resp.json()
    tours_resp = tours_json['SearchResult']['SearchResultItems']
    tours_list = list()
    for tour_orig in tours_resp:
        # time
        t = tour_orig['DepartureDate']
        time = "%s-%s-%s" % (t[6:10], t[3:5], t[0:2])

        # hotel
        hotel = dict()
        hotel['name'] = tour_orig['HotelName']
        hotel['url'] = 'http://www.tui.ua' + tour_orig['HotelUrl']
        # images
        images = list()
        for i in tour_orig['Photos']:
            images.append('http://www.tui.ru/CmsPages/GetPhoto.aspx/?fileguid=' + i)
        hotel['images'] = images

        # create object
        tour = dict()
        tour['country'] = tour_orig['CountryName']
        tour['country_id'] = tour_orig['CountryId']
        tour['date_start'] = time
        tour['nights'] = tour_orig['Nights']
        tour['adults'] = tour_orig['Adults']
        tour['children'] = tour_orig['Children']
        tour['meals'] = convert_meal(tour_orig['PansionName'])
        tour['price'] = tour_orig['Price']
        tour['hotel'] = hotel
        tour['agent'] = 'tui'
        tour['booking_url'] = tour_orig['BookingUrl']
        tours_list.append(tour)

    response = dict()
    response['count_items'] = tours_json['SearchResult']['TotalItems']
    response['data'] = tours_list
    return response
    # return json.dumps(tours_list, ensure_ascii=False)