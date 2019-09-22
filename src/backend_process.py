import requests
from geopy.geocoders import Nominatim
from pymongo import MongoClient
from scipy.ndimage.interpolation import shift
from pprint import pprint
import numpy as np
import datetime
import time

class Event:
    #'within' is not in results dictionary
    def __init__(self, rank, ID, title, desc, category, entities, location, state, duration):
        self.rank = rank
        self.ID = ID
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
    time.sleep(2)
    myquery = {"pending": True}
    assignment_collection.delete_many(myquery)
    
#dtakes in (xlong,ylat) which is center of square. ef assignLocation:
def assignLocation(x,y,drivers):
    tuple_list = list()
    #1 degree of longitude ~=~ 55.051 miles? assuming latitude is the same
    #l is length of the square in degrees
    l = 10/55.051
    #number of sub-squares
    a = np.sqrt(drivers)

    long_array = np.linspace(start = x-l/2, stop = x+l/2, num = a+1)
    long_array1 = shift(long_array,-1,cval=0)
    long_array = (long_array+long_array1)/2
    long_array = np.resize(long_array,(1,int(a))).flatten()

    lat_array = np.linspace(start = y-l/2, stop = y+l/2, num = a+1)
    lat_array1 = shift(lat_array,-1,cval=0)
    lat_array = (lat_array+lat_array1)/2
    lat_array = np.resize(lat_array,(1,int(a))).flatten()

    for _ in range(drivers):
        random_squarex = np.random.randint(int(a))
        random_squarey = np.random.randint(int(a))
        xc = long_array[random_squarex]
        yc = lat_array[random_squarey]
        driver_tuple = (xc, yc)
        tuple_list.append(driver_tuple)
    return tuple_list

#sida is number of regions inside the squaredef aain():
    #find x value
    #y_array=np.li
    #one degree of longitude = 55.051 miles?????nspace(start = 0, end = , num = a)

def get_locs (events, database):
    locs = {}
    for event in events:
        myquery = {"zipCode": int(event.zipcode)}
        results = database.count_documents(myquery)
        locs.update( {event.zipcode : assignLocation(event.location[0],event.location[1], results)} )
    return locs

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
    filtered_events = list(filter(lambda x: x.zipcode.isdigit(), events))

    print("\n")
    print("connecting to database...")
    # connect to MongoDB
    client = MongoClient("mongodb://admin:admin123@cluster0-shard-00-00-au5yo.mongodb.net:27017,cluster0-shard-00-01-au5yo.mongodb.net:27017,cluster0-shard-00-02-au5yo.mongodb.net:27017/hestia?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.hestia

    driver_collection = db.hestia_users
    assignment_collection = db.hestia_assignments
    events_collection = db.hestia_events

    locations = get_locs(filtered_events, driver_collection)

    print("\n")
    for x in driver_collection.find():
        driver_zipcode = x["zipCode"]

        drive_zip = [(y, y.zipcode) for y in filtered_events]

        for (event,zipcode) in drive_zip:

            if driver_zipcode == int(zipcode):
                
                isIn = False

                for z in assignment_collection.find():
                    if z["_id"] == x["_id"]:
                        isIn = True
                        
                if(not isIn):
                
                    assigned_driver = { 
                    '_id': x["_id"],  
                    'driver': x["fullName"],
                    'event': {'eventId': event.ID, 
                              'address': str(event.address),
                              'latitude': locations[event.zipcode][0][0],
                              'longitude': locations[event.zipcode][0][1]}, 
                    'created': datetime.datetime.now(),
                    'pending': True
                    }
                    locations[event.zipcode].pop(0)

                    assignment_collection.insert_one(assigned_driver)
                    
    for e in events:
        new_event = { 
                    'eventId': e.ID,  
                    'address': e.address,
                    'latitude': e.location[0],
                    'longitude': e.location[1] 
                    }
        events_collection.insert_one(new_event) 

    #Moved delay to method
    for _ in range(3):
        eliminate_done(assignment_collection)

if __name__ == "__main__":
    main()
    while(False):
        main()
        