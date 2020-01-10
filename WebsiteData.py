from configparser import ConfigParser
import pymongo
import dns

class WebsiteData:
    guests = []
    duplicates = []
    
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
    def getGuests(self):
        profiles = list(self.profileCollection.find())
        users = list(self.usersCollection.find())
        
        print('--------------------------------------------------------------\nGuests\n')
        for rsvp in profiles:
            if rsvp['status'] == 'Accept':
                # Push user's name in guests list
                for user in users:
                    if rsvp['user'] == user['_id']:
                        self.guests.append(user['name'])
                
                # Push guests' name into guests list as well...
                for guest in rsvp['guests']:
                    self.guests.append(guest['name'])

        self.removeDups(self.guests, len(self.guests))
    
    def removeDups(self, guestList, n):
        mp = { i : 0 for i in guestList}
        count = 0

        for i in range(n):
            if mp[guestList[i]] == 0:
                print(guestList[i], end = "\n")
                count += 1
                mp[guestList[i]] = 1
            else:
                self.duplicates.append(guestList[i])

        print('\nTotal number of guests: ', count)
    
    # Show all duplicate names found in database
    def showDuplicates(self):
        print('\n**Duplicate names in DB**')
        for name in self.duplicates:
            print(name)
    
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
