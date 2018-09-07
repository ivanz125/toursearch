from pymongo import MongoClient


class Database:

    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        self.db = client.tours
        self.tours_collection = self.db.tours_selena

    def clear_data(self):
        r = self.tours_collection.delete_many({})
        print(r.deleted_count, " docs deleted")

    def get_all_tours(self):
        tours = self.tours_collection.find({})
        result = list()
        for tour in tours:
            print(tour)
            tour.pop('_id', None)
            result.append(tour)
        return result
