import requests
from geopy.geocoders import Nominatim

class Event:

    #'within' is not in results dictionary
    def __init__(self, id, title, desc, category, entities, location, state, duration):
        self.id = id
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
        "category": ["severe-weather","disasters"]
    }
)

responses = response.json()

events = list()
for item in responses["results"]:
    events.append(Event(item["id"], item["title"], item["description"], item["category"], item["entities"], item["location"], item["state"], item ["duration"]))


geolocator = Nominatim()


for ii in events:
    new_loc = str(ii.location[1]) + ", " + str(ii.location[0])
    location = geolocator.reverse(new_loc)
    print("\n")
    print(ii.title)
    print(location.address)
    print("\n")


