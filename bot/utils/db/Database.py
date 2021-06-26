import pymongo
import loader
from .User import User
from .. import config
# from ... import loader

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
            # return self.users.find_one({"user_id": user_id}).get("cards")
            return self.users.find_one({"user_id": user_id}, {"username": True, "first_name": True, "last_name": True})
        except AttributeError:
            return dict()

    def get_cards_from_group(self, group_id: int): # -> Dict[int, Dict[int, str]]:
        list_of_users_object_id = (self._get_users_with_cards_from_group(group_id))[0]
        list_of_user_object_user = (self._get_users_with_cards_from_group(group_id))[1]
        list_of_users = dict()
        for i, user_object_id in enumerate(list_of_users_object_id):
            user = self.users.find_one({"_id": user_object_id}, {"user_id": True, "cards": True})
            user_info = list_of_user_object_user[i]
            user_cards = user["cards"]
            list_of_users[user_info] = user_cards
        return list_of_users

    def _get_users_with_cards_from_group(self, group_id: int):  # -> list[int]:
        list_of_users_in_group = list()
        user_object_user = list()
        for user in self.users.find({"cards": {"$ne": {}}}, {"_id": True, "user_id": True, "first_name": True,
                                                             "last_name": True}):
            user_id = user["user_id"]
            user_object_id = user["_id"]
            user_last_name = user["last_name"]
            user_first_name = user["first_name"]

            if loader.bot.get_chat_member(chat_id=group_id, user_id=user_id):
                user_object_user.append(str(user_first_name) + " " + str(user_last_name))
                list_of_users_in_group.append(user_object_id)
        return [list_of_users_in_group, user_object_user]

    def get_user_name_from_group(self, group_id: int):
        names = self._get_users_with_cards_from_group(group_id)[1]
        ids = self._get_users_with_cards_from_group(group_id)[0]
        k = list(zip(names, ids))
        return k




