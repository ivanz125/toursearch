from flask import Flask
from flask import jsonify
from flask import request
import json
import requests

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


def convert_meal_tui(name):
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


@app.route("/")
def hello():
    # return "Hello World!"
    r = requests.get('https://api.github.com/events')
    return r.text


@app.route("/tui")
def search_tui():
    country_id = request.args.get('id_country', default=1, type=int)

    params = {'adult':2, 'checkinBegin':20180910, 'checkinEnd':20180914, 'child':0, 'currency':4, 'groupByHotel':True,
              'isRuSite':False, 'nightMax':4, 'nightMin':3, 'pageNum':1, 'pageSize':1,
              'state':-18803, 'townFrom':235144}
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
        tour['meals'] = convert_meal_tui(tour_orig['PansionName'])
        tour['price'] = tour_orig['Price']
        tour['hotel'] = hotel
        tour['booking_url'] = tour_orig['BookingUrl']
        tours_list.append(tour)

    response = dict()
    response['count_items'] = tours_json['SearchResult']['TotalItems']
    response['data'] = tours_list
    return jsonify(response)
    # return json.dumps(tours_list, ensure_ascii=False)


@app.route("/hello")
def hello_f():
    response = requests.get("https://jsonplaceholder.typicode.com/todos")
    return response.json()[1]['title']


if __name__ == '__main__':
    app.run(debug=True)