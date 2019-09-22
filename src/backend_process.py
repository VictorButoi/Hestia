import requests
from geopy.geocoders import Nominatim
from pymongo import MongoClient
from pprint import pprint
import datetime
import time

class Event:
    #'within' is not in results dictionary
    def __init__(self, rank, id, title, desc, category, entities, location, state, duration):
        self.rank = rank
        self.id = id
        self.title = title
        self.desc = desc
        self.category = category
        self.entities = entities
        self.location = location
        self.state = state
        self.duration = duration
        self.zipcode = ""
        self.address = ""

def eliminate_done(assignment_collection):
    myquery = {"pending": True}
    assignment_collection.delete_many(myquery)

def main():
    response = requests.get(
        url="https://api.predicthq.com/v1/events/",
        headers={
        "Authorization": "Bearer GdyEbabHRui-VxV-IKlLRxUkS81OvluuryGG51uZ",
        "Accept": "application/json"
        },
        params={
            "country": "US",
            "rank_level": 5,
            "category": "severe-weather",
            "state": "active"
        }
    )

    responses = response.json()

    events = list()
    for item in responses["results"]:
        events.append(Event(item["id"], item["rank"], item["title"], item["description"], item["category"], item["entities"], item["location"], item["state"], item ["duration"]))

    geolocator = Nominatim()

    for ii in events:

        new_loc = str(ii.location[1]) + ", " + str(ii.location[0])
        location = geolocator.reverse(new_loc)
        ii.address=location

        zipcode = location.address.split(", ")[-2].strip()
        zipcode = zipcode.split(":")[0]
        ii.zipcode=zipcode

    #remove events without zipcodes
    for item in events:
        if(not(item.zipcode.isdigit())):
            events.remove(item)
            del item
        else:
            print(item.zipcode)

    print("\n")
    print("connecting to database...")
    # connect to MongoDB
    client = MongoClient("mongodb://admin:admin123@cluster0-shard-00-00-au5yo.mongodb.net:27017,cluster0-shard-00-01-au5yo.mongodb.net:27017,cluster0-shard-00-02-au5yo.mongodb.net:27017/hestia?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.hestia
    driver_collection = db.hestia_users
    assignment_collection = db.hestia_assignments

    print("\n")
    for x in driver_collection.find():
        driver_zipcode = x["zipCode"]

        drive_zip = [(y, y.zipcode) for y in events]

        for (event,zipcode) in drive_zip:

            if driver_zipcode == int(zipcode):


                if(dict(filter(lambda z: z["_id"] == x["_id"], assignment_collection.find())) == {}):
                
                    assigned_driver = { 
                    '_id': x["_id"],  
                    'driver': x["fullName"],
                    'event': {'eventId': event.id, 'address': str(event.address)}, 
                    'created': datetime.datetime.now(),
                    'pending': True
                    }

                    print("hit")
                    
                    assignment_collection.insert_one(assigned_driver)

                    for x in assignment_collection.find():
                        print(x["fullName"])

    
    time.sleep(2)
    eliminate_done(assignment_collection)
    time.sleep(2)
    eliminate_done(assignment_collection)
    time.sleep(2)
    eliminate_done(assignment_collection)

if __name__ == "__main__":
    main()
    while(False):
        main()
        