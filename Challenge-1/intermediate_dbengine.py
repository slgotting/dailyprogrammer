
import pymongo
from pymongo import MongoClient




class MongoEngine:
    def __init__(self, db='events', collection='events', host='mongodb://127.0.0.1:27017'):
        try:
            self.client = MongoClient(host)
        except:
            print("Could not connect to MongoDB")

        self.db = self.client[db]
        self.collection = self.db[collection]

    @classmethod
    def establish_connection(cls, host):
        return cls(host=host)

    def change_collection(self, new_coll):
        self.collection = new_coll

    def retrieve_all_from_coll(self):
        return list(self.collection.find())

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
            if self.collection.find({'id': i}) == None:
                return i
            i+=1
        return i

    def get_every_key_in_collection(self):
        keys = []
        for obj in list(self.collection.find()):
            for key in obj.keys():
                if key not in keys:
                    keys.append(key)

        #keys = [key for key not in obj.keys() for obj in list(self.collection.find())]

        return keys
