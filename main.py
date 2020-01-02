from configparser import ConfigParser
import pymongo
import dns

class websiteData:
    numGuests = 0

    def __init__(self):
        self.parser = ConfigParser()
        
        self.parser.read('default.ini')
        
        self.connection = pymongo.MongoClient(self.parser.get('db', 'mongoURI'))

        self.database = self.connection['test']
        self.collection = self.database['profiles']

    # Counts guests who have accepted their invitations, as well as their guests
    def countGuests(self):
        col = list(self.collection.find())

        for doc in col:
            if doc['status'] == 'Accept':
                self.numGuests += (1 + len(doc['guests']))

        return self.numGuests
    
    # Counts food items
    def countFood(self):
        pass

