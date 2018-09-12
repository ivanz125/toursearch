import requests
from tours import utils


def id_country_for_tez(code):
    if code == 'bg':
        return 158976
    elif code == 'gr':
        return 7067498
    elif code == 'ge':
        return 1001354
    elif code == 'do':
        return 111241
    elif code == 'eg':
        return 5732
    elif code == 'il':
        return 143785
    elif code == 'id': # Indonesia
        return 158062
    elif code == 'es':
        return 5733
    elif code == 'it':
        return 154020
    elif code == 'cy':
        return 7067673
    elif code == 'cn': # China
        return 140009
    elif code == 'cu': # Cuba
        return 111137
    elif code == 'lv':
        return 146695
    elif code == 'lt':
        return 160820
    elif code == 'mu': # Mauritius
        return 3013008
    elif code == 'mv': # Maldives
        return 166775
    elif code == 'mx':
        return 162875
    elif code == 'ae':
        return 7067149
    elif code == 'pt':
        return 132579
    elif code == 'sc': # Seychelles
        return 6030845
    elif code == 'th': # Thailand
        return 12695
    elif code == 'tr':
        return 1104
    elif code == 'fr':
        return 136683
    elif code == 'lk': # Sri Lanka
        return 138865
    elif code == 'ee':
        return 513974
    return 0


# Convert date in format YYYYMMDD to DD.MM.YYYY
def date_for_tez(date):
    d = str(date)
    return d[6:8] + '.' + d[4:6] + '.' + d[0:4]


def adults_children_for_tez(adults, children):
    if adults == 1 and children == 0:
        return 1
    elif adults == 1 and children == 1:
        return 14317
    elif adults == 1 and children == 2:
        return 14357
    elif adults == 2 and children == 0:
        return 2
    elif adults == 2 and children == 1:
        return 14258
    elif adults == 2 and children == 2:
        return 14356
    elif adults == 3 and children == 0:
        return 3
    elif adults == 3 and children == 1:
        return 21347
    elif adults == 3 and children == 2:
        return 26274
    elif adults == 4 and children == 0:
        return 15352
    elif adults == 4 and children == 1:
        return 26275
    elif adults == 4 and children == 2:
        return 31212
    elif adults == 5 and children == 0:
        return 26273
    elif adults == 5 and children == 1:
        return 67982
    elif adults == 5 and children == 2:
        return 67983
    elif adults == 6 and children == 0:
        return 15351
    elif adults == 6 and children == 1:
        return 149641
    elif adults == 6 and children == 2:
        return 152854
    elif adults == 7 and children == 0:
        return 63356
    elif adults == 7 and children == 1:
        return 115051
    elif adults == 8 and children == 0:
        return 150677
    return 0


def meals_for_tez(meals):
    # Should use rAndBBetter=false is other not specified
    if meals == 'ai': # Also Ultra AI 5738, need to include rAndBBetter=true
        return 5737
    elif meals == 'bb':
        return 2424
    elif meals == 'fb':
        return 2749
    elif meals == 'hb':
        return 2474
    elif meals == 'ro':
        return 15350
    return 0


def get_results(code_country, start_date_from, start_date_to, adults, children, b_day_1, b_day_2,
                nights_min, nights_max, meals, price_max=0):
    params = {'currency': 46688, 'tourType': 1, 'locale': 'ru', 'cityId': 3667, 'rAndBBetter': False,
              'noTicketsTo': False, 'noTicketsFrom': False, 'priceMin': 0,
              'hotelClassId': 269506, 'hotelClassBetter': True, 'formatResult': True}

    # max price
    if price_max > 0:
        params['priceMax'] = price_max
    else:
        params['priceMax'] = 1500000
    params['countryId'] = id_country_for_tez(code_country)
    params['after'] = date_for_tez(start_date_from)
    params['before'] = date_for_tez(start_date_to)
    params['nightsMin'] = nights_min
    params['nightsMax'] = nights_max
    params['accommodationId'] = adults_children_for_tez(adults, children)
    params['rAndBId'] = meals_for_tez(meals)
    if meals == 'ai':
        params['rAndBBetter'] = True
    if children > 0:
        params['birthday1'] = date_for_tez(b_day_1)
    if children > 1:
        params['birthday2'] = date_for_tez(b_day_2)

    results = dict()
    results['count_items'] = 0
    results['data'] = list()
    for i in range(5):
        resp = requests.get('http://search.tez-tour.com/tariffsearch/getResult', params=params)
        tours_json = resp.json()
        if not tours_json['success']:
            results['fail_%s' % i] = tours_json['message']
            continue
        new_min_price = get_results_page(resp, results, code_country, adults, children)
        # no more items
        if new_min_price == 0:
            break
        # load next items
        params['priceMin'] = new_min_price

    return results


def get_results_page(resp, results, code_country, adults, children):
    tours_json = resp.json()
    if not tours_json['success']:
        response = dict()
        response['count_items'] = 0
        response['data'] = []
        response['fail'] = tours_json['message']
        return response

    tours_resp = tours_json['data']
    tours_list = results['data']
    for tour_orig in tours_resp:
        # time
        t = tour_orig[0]
        time = "%s-%s-%s" % (t[6:10], t[3:5], t[0:2])

        # hotel
        h = tour_orig[6]
        hotel = dict()
        hotel['name'] = h[1]
        hotel['url'] = h[0]
        # images
        images = list()
        images.append(h[2])
        hotel['images'] = images

        # booking url
        base_url = tour_orig[11][0][0]
        dep_city = tours_json['departureCityId']
        date_from = tour_orig[0]
        night_count = tour_orig[3]
        hotel_u = h[3]
        price = int(tour_orig[10]['total'])
        early_booking = tour_orig[14]['earlyBooking']['value']
        booking_url = "https://www.tez-tour.com/ru/kiev/search/applicationForm.html?booklink=%s&departureCity=%s" \
                      "&dateFrom=%s&nightCount%s&hotel=%s&price=%s&currency=46688&buyOnline=true&earlyBooking=%s"
        booking_url = booking_url % (base_url, dep_city, date_from, night_count, hotel_u, price, early_booking)

        # create object
        tour = dict()
        tour['country'] = utils.country_name(code_country)
        tour['date_start'] = time
        tour['nights'] = tour_orig[3]
        tour['adults'] = adults
        tour['children'] = children
        tour['meals'] = tour_orig[7][0]
        tour['price'] = price
        tour['hotel'] = hotel
        tour['agent'] = 'tez'
        tour['booking_url'] = booking_url
        tours_list.append(tour)

    results['count_items'] = results['count_items'] + int(tours_json['info'][1][1])

    # more results present, return price of last result +1
    if tours_json['info'][3][1] and len(tours_list) > 0:
        return tours_list[len(tours_list) - 1]['price'] + 1
    return 0
    #response = dict()
    #response['count_items'] = tours_json['info'][1][1]
    #response['data'] = tours_list
    #return response
