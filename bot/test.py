import pymongo
from bson import ObjectId

from bot.utils import config
from bot.utils.db.Purchase import Purchase

username = config.DATABASE_USERNAME
password = config.DATABASE_PASSWORD

client = pymongo.MongoClient(
            f"mongodb+srv://{username}:{password}@share-bot.pqplb.mongodb.net/myFirstDatabase?retryWrites=true"
            f"&w=majority")
database = client.get_database("Database")
users = database.get_collection("users")
purchases = database.get_collection("purchases")

user_id = 395589642
purchase_id = "60cf60121107ee03c18795cf"

list_of_payers = purchases.find_one({"_id": ObjectId(purchase_id)})["payers"]
print(list_of_payers)
if list_of_payers is None:
    print("None")
else:
    print(user_id in list_of_payers)
