import pymongo
from . import User
from .. import config

username = config.DATABASE_USERNAME
password = config.DATABASE_PASSWORD


class DataBase:
    def __init__(self):
        self.client = pymongo.MongoClient(
            f"mongodb+srv://{username}:{password}@share-bot.pqplb.mongodb.net/myFirstDatabase?retryWrites=true"
            f"&w=majority")
        # self.users = client.users

    def add_user(self, user: User):
        self.client.Users.user.insert_one(vars(user))

    def find_user_by_telegram_id(self, user_id: int):
        return self.client.Users.user.find_one({"user_id": user_id})
