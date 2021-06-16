import pymongo
import logging

logging.basicConfig(level=logging.DEBUG)

username = ""
password = ""

client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@share-bot.pqplb.mongodb.net/myFirstDatabase"
                             "?retryWrites=true&w=majority")
db = client.users

