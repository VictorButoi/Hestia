import requests
from geopy.geocoders import Nominatim

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




#we have to query database to get drivers, and see if any are compatible with event zipcodes