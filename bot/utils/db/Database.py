import pymongo
from . import User
from .. import config

username = config.DATABASE_USERNAME
password = config.DATABASE_PASSWORD


class DataBase:
    def __init__(self):
        self._client = pymongo.MongoClient(
            f"mongodb+srv://{username}:{password}@share-bot.pqplb.mongodb.net/myFirstDatabase?retryWrites=true"
            f"&w=majority")
        self._database = self._client.get_database("Database")
        self.users = self._database.get_collection("users")

    def add_user(self, user: User):
        self.users.insert_one(vars(user))

    def find_user_by_telegram_id(self, user_id: int) -> dict:
        try:
            return self.users.find_one({"user_id": user_id})
        except AttributeError:
            return dict()

    def add_user_card(self, user_id: int, card: int, bank: str = None):
        self.users.update_one({"user_id": user_id}, {"$set": {"cards." + str(card): bank}})

    def del_user_card(self, user_id: int, card: int):
        self.users.update_one({"user_id": user_id}, {"$unset": {"cards." + str(card): ""}})

    def get_user_cards(self, user_id: int) -> dict:
        try:
            return self.users.find_one({"user_id": user_id}).get("cards")
        except AttributeError:
            return dict()

    def get_users_from_group(self, group_id: int) -> pymongo.cursor:
        pass
