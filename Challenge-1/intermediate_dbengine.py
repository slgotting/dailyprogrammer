

from pymongo import MongoClient




class MongoEngine:
    def __init__(self, db='events', host=''):
        try:
            self.client = MongoClient(host)
        except:
            print("Could not connect to MongoDB")

        self.db = self.client[db]

    @classmethod
    def establish_connection(cls, host):
        return cls(host=host)

    def retrieve_all_from_db():
        pass

    def filter_date_range(start_date, end_date):
        pass

    def add_to_db(self, event_json):
        self.db.insert_one(
        