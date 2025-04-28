from pymongo import MongoClient


class Storage:
    def __init__(self, uri="mongodb://mongodb:27017/", db_name="waze_data"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["events"]

    def insert_events(self, events):
        if events:
            self.collection.insert_many(events)

    def find_events(self, query={}, limit=10):
        return list(self.collection.find(query).limit(limit))
