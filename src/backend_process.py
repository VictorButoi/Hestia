import requests
from geopy.geocoders import Nominatim
from pymongo import MongoClient
from pprint import pprint

class Event:

    #'within' is not in results dictionary
    def __init__(self, rank, id, title, desc, category, entities, location, state, duration):
        self.id = id
        self.rank = rank
        self.title = title
        self.desc = desc
        self.category = category
        self.entities = entities
        self.location = location
        self.state = state
        self.zipcode = ""
        self.duration = duration

response = requests.get(
    url="https://api.predicthq.com/v1/events/",
    headers={
      "Authorization": "Bearer GdyEbabHRui-VxV-IKlLRxUkS81OvluuryGG51uZ",
      "Accept": "application/json"
    },
    params={
        "country": "US",
        "rank_level": 5,
        "category": ["severe-weather"]
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

    zipcode = location.address.split(", ")[-2].strip()
    zipcode = zipcode.split(":")[0]
    ii.zipcode=zipcode

#remove events without zipcodes
for item in events:
    if(not(item.zipcode.isdigit())):
        events.remove(item)
        del item

print("\n")
print("connecting to database...")
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb://admin:admin123@cluster0-shard-00-00-au5yo.mongodb.net:27017,cluster0-shard-00-01-au5yo.mongodb.net:27017,cluster0-shard-00-02-au5yo.mongodb.net:27017/hestia?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.hestia
driver_collection = db.hestia_users
assignment_collection = db.hestia_assignments
print("\n")
for x in driver_collection.find():
  print(x["zipCode"])



for ii in assignment_collection.find():
    print(ii)

