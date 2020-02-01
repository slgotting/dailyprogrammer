

from pymongo import MongoClient




class MongoEngine:
    def __init__(self, db='events', collection='events', host=''):
        try:
            self.client = MongoClient(host)
        except:
            print("Could not connect to MongoDB")

        self.db = self.client[db]
        self.collection = self.db[collection]

    @classmethod
    def establish_connection(cls, host):
        return cls(host=host)

    def retrieve_all_from_db():
        pass

    def filter_date_range(start_date, end_date):
        pass

    def filter_by_mongo_args(*args):
        self.collection.find(args)

    def add_to_db(self, event_json):
        self.collection.insert_one(event_json)
        
    def remove_all(self, json):
        self.collection.delete_many(json)
    
    def sort_by(self, *args):
        return list(self.collection.find({}).sort(*args))
    
    def collection_length(self):
        return self.collection.count()
    
    def first_empty_id(self, i=0):
        while i < self.collection_length():
            if not self.collection.find({'id': i}):
                return i
            i+=1
        return i
