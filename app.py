from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient(
    "mongodb://root:g%40Y3022D%4016C@192.168.1.8:52115/?authSource=admin&readPreference=primary&authMechanism=DEFAULT&appname=MongoDB%20Compass&directConnection=true&ssl=false"
)

db = client["sa_dev"]

_id = ObjectId("65de1bcee1be5c3a9d360315")
collection = db["plans"]
match_query = {"type": "plan", "_id": _id}
timestamp = int(datetime.utcnow().timestamp())
# get plan from db
plan = collection.find_one(match_query)
versions = plan["versions"]
latest_version = versions[-1]
latest_version["revision"] = len(versions) + 1
latest_version["created_at"] = timestamp

# write plan to db
collection.update_one(
    match_query,
    {
        "$push": {"versions": latest_version},
        "$set": {
            "updated_at": latest_version["created_at"],
        },
        "$inc": {"revision": 1},
    },
)

print(plan)