from configparser import ConfigParser
import pymongo
import dns

class WebsiteData:
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
        
        print('--------------------------------------------------------------')
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
        totalGuests = self.countGuests()
        
        print('Guest List\n')
        if self.numOfGuests > 0:
            for guest in self.guests:
                print(guest)
        else:
            print('None')
        
        print('\nTotal Number of Guests: ', totalGuests)

    def countFood(self):
        profiles = list(self.profileCollection.find())

        print('--------------------------------------------------------------\nFood\n')
        for rsvp in profiles:
            if rsvp['status'] == 'Accept':
                if rsvp['food'] == 'Beef':
                    self.beef += 1
                elif rsvp['food'] == 'Chicken':
                    self.chicken += 1
                elif rsvp['food'] == 'Fish':
                    self.fish += 1
                elif rsvp['food'] == 'Vegetarian':
                    self.vegetarian += 1
                elif rsvp['food'] == 'kidsMeal':
                    self.kidsMeal += 1
                
                for guest in rsvp['guests']:
                    if guest['food'] == 'Beef':
                        self.beef += 1
                    elif guest['food'] == 'Chicken':
                        self.chicken += 1
                    elif guest['food'] == 'Fish':
                        self.fish += 1
                    elif guest['food'] == 'Vegetarian':
                        self.vegetarian += 1
                    elif guest['food'] == 'kidsMeal':
                        self.kidsMeal += 1
        print('Chicken: ', self.chicken)
        print('Beef: ', self.beef)
        print('Fish: ', self.fish)
        print('Vegetarian: ', self.vegetarian)
        print('Kids\'s meal: ', self.kidsMeal)

