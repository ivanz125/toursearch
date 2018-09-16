from database import mongo
from tours import utils
import datetime


class Database:

    def __init__(self):
        self.db = mongo.client.tours
        self.tours_collection = self.db.tours_selena

    def clear_data(self):
        r = self.tours_collection.delete_many({})
        print(r.deleted_count, " docs deleted")

    def get_all_tours(self):
        tours = self.tours_collection.find({})
        tours_list = list()
        for tour in tours:
            tour.pop('_id', None)
            tour.pop('description', None)
            tours_list.append(tour)
        result = dict()
        result['count_items'] = len(tours_list)
        result['data'] = tours_list
        return result

    def get_tours(self, days_min, days_max, price=1000000, places='', places_mode='one', date_min=0, date_max=0):
        max_price_uah = price / utils.uah_to_eur_rate(self.db)
        params = {"$or": [
            {"currency": "EUR", "price": {"$lte": price}, "days": {"$gte": days_min, "$lte": days_max}},
            {"currency": "UAH", "price": {"$lte": max_price_uah}, "days": {"$gte": days_min, "$lte": days_max}},
        ]}
        tours = self.tours_collection.find(params)
        tours_list = list()
        for tour in tours:
            tour.pop('_id', None)
            tour.pop('description', None)
            if places != '' and places_mode == 'one' and (not check_places_one(places, tour['places'])):
                continue
            if places != '' and places_mode == 'all' and (not check_places_all(places, tour['places'])):
                continue
            if date_min != 0 and date_max != 0 and (not check_dates(date_min, date_max, tour)):
                continue
            tours_list.append(tour)
        result = dict()
        result['count_items'] = len(tours_list)
        result['data'] = tours_list
        return result

    def get_one_tour(self, url):
        tour = self.tours_collection.find_one({'url': url})
        if tour is not None:
            tour.pop('_id', None)
        return tour


def check_places_one(places_str, tour_places):
    places = places_str.split(',')
    places = [p.strip() for p in places]
    for name in places:
        name = name.lower()
        for tp in tour_places:
            tp = tp.lower()
            if name in tp or tp in name:
                return True
    return False


def check_places_all(places_str, tour_places):
    places = places_str.split(',')
    places = [p.strip() for p in places]
    print(places)
    for name in places:
        match = False
        name = name.lower()
        for tp in tour_places:
            tp = tp.lower()
            if name in tp or tp in name:
                match = True
                break
        if not match:
            return False
    return True


def check_dates(date_min, date_max, tour):
    floor = utils.date_int_to_datetime(date_min)
    ceil = utils.date_int_to_datetime(date_max)
    for date in tour['dates']:
        d = datetime.date(int(date[6:10]), int(date[3:5]), int(date[0:2]))
        if floor <= d <= ceil:
            return True
    return False
