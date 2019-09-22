from pymongo import MongoClient

print("connecting to database...")
# connect to MongoDB
client = MongoClient("mongodb://admin:admin123@cluster0-shard-00-00-au5yo.mongodb.net:27017,cluster0-shard-00-01-au5yo.mongodb.net:27017,cluster0-shard-00-02-au5yo.mongodb.net:27017/hestia?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.hestia
driver_collection = db.hestia_users
assignment_collection = db.hestia_assignments

for x in driver_collection.find():
    print(x["fullName"])

print("this is right")

for x in assignment_collection.find():
    print(x["fullName"])