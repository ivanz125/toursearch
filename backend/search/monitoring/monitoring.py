from database import mongo
from tours import tours_general
import datetime
from tours import utils
from urllib.parse import unquote


def create(params):
    code_country = params.get('code_country', default='', type=str)
    start_date_from = params.get('start_date_from', default=20180920, type=int)
    start_date_to = params.get('start_date_to', default=20180923, type=int)
    adults = params.get('adults', default=2, type=int)
    children = params.get('children', default=0, type=int)
    b_day_1 = params.get('b_day_1', default=20050801)
    b_day_2 = params.get('b_day_2', default=20070801)
    nights_min = params.get('nights_min', default=6, type=int)
    nights_max = params.get('nights_max', default=7, type=int)
    meals = params.get('meals', default='bb', type=str)
    price_max = params.get('price_max', default=0, type=int)
    price_limit = params.get('price_limit', default=25000, type=int)
    monitoring_id = params.get('id', default=0, type=int)
    user_id = params.get('user_id', default=0, type=int)
    name = unquote(params.get('name', default='Monitoring', type=str))
    monitoring_type = params.get('type', default='', type=str)
    if monitoring_id == 0 or (monitoring_type != 'avia' and monitoring_type != 'bus'):
        return 0

    monitoring = dict()
    monitoring['id'] = monitoring_id
    monitoring['user_id'] = user_id
    monitoring['name'] = name
    monitoring['params'] = dict()
    monitoring['results'] = list()
    monitoring['params']['type'] = monitoring_type
    monitoring['params']['code_country'] = code_country
    monitoring['params']['start_date_from'] = start_date_from
    monitoring['params']['start_date_to'] = start_date_to
    monitoring['params']['adults'] = adults
    monitoring['params']['children'] = children
    if children > 0:
        monitoring['params']['b_day_1'] = b_day_1
    if children > 1:
        monitoring['params']['b_day_2'] = b_day_2
    monitoring['params']['nights_min'] = nights_min
    monitoring['params']['nights_max'] = nights_max
    monitoring['params']['price_max'] = price_max
    monitoring['params']['price_limit'] = price_limit
    monitoring['params']['meals'] = meals
    monitoring['params']['meals'] = meals

    db = mongo.client.tours
    db.monitoring.insert_one(monitoring)
    return 1


def execute(monitoring_id):
    db = mongo.client.tours
    monitoring = db.monitoring.find_one({"id": monitoring_id})
    if monitoring is None:
        return {'results': -1, 'error': 'No monitoring with id ' + str(monitoring_id)}
    if monitoring['params']['type'] == 'avia':
        code_country = monitoring['params']['code_country']
        start_date_from = monitoring['params']['start_date_from']
        start_date_to = monitoring['params']['start_date_to']
        adults = monitoring['params']['adults']
        children = monitoring['params']['children']
        b_day_1 = monitoring['params'].get('b_day_1', 20050801)
        b_day_2 = monitoring['params'].get('b_day_2', 20070801)
        nights_min = monitoring['params']['nights_min']
        nights_max = monitoring['params']['nights_max']
        meals = monitoring['params']['meals']
        price_max = monitoring['params']['price_max']
        price_limit = monitoring['params']['price_limit']
        results = tours_general.get_tours_avia(code_country, start_date_from, start_date_to, adults, children,
                                               b_day_1, b_day_2, nights_min, nights_max, meals, price_max)
        data = results['data']
        passed = list()
        for tour in data:
            if tour['price'] <= price_limit:
                passed.append(tour)
        entry = dict()
        entry['time'] = datetime.datetime.now().timestamp()
        entry['results_count'] = len(passed)
        entry['results'] = passed
        if 'results' not in monitoring:
            monitoring['results'] = list()
        monitoring['results'].append(entry)

        db.monitoring.update_one({"id": monitoring_id}, {"$set": monitoring})
        return {'results': len(passed), 'data': passed}


def get(user_id):
    db = mongo.client.tours
    results = db.monitoring.find({"user_id": user_id})
    monitoring_list = list()
    for monitoring in results:
        monitoring.pop('_id', None)
        monitoring.pop('results', None)
        monitoring['country'] = utils.country_name(monitoring['params']['code_country'])
        # for res in monitoring['results']:
        #    res.pop('results')
        monitoring_list.append(monitoring)
    return monitoring_list

