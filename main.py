from configparser import ConfigParser
import pymongo
import dns

class websiteData:
    numOfGuests = 0
    guests = []
    
    chicken = 0
    beef = 0
    fish = 0
    vegetarian = 0
    kidsMeal = 0

    def __init__(self):
        self.parser = ConfigParser()
        
        self.parser.read('default.ini')
        
        self.connection = pymongo.MongoClient(self.parser.get('db', 'mongoURI'))

        self.database = self.connection['test']
        self.profileCollection = self.database['profiles']
        self.usersCollection = self.database['users']

    # Counts guests who have accepted their invitations, as well as their guests
    def countGuests(self):
        profiles = list(self.profileCollection.find())
        users = list(self.usersCollection.find())

        for rsvp in profiles:
            if rsvp['status'] == 'Accept':
                self.numOfGuests += (1 + len(rsvp['guests']))

                # Push user's name in guests list
                for user in users:
                    if rsvp['user'] == user['_id']:
                        self.guests.append(user['name'])
                
                # Push guests' name into guests list as well...
                for guest in rsvp['guests']:
                    self.guests.append(guest['name'])
        
        return self.numOfGuests
    
    def getGuests(self):
        for guest in self.guests:
            print(guest)


if __name__ == '__main__':
    data = websiteData()

    totalGuests = data.countGuests()

    print('Guest List:')
    data.getGuests()

    print('\nTotal Number of People Attending Wedding: ', totalGuests)

