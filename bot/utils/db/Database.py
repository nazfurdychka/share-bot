import pymongo
from .User import User
from .Purchase import Purchase
from .. import config
import loader

from bson import ObjectId

username = config.DATABASE_USERNAME
password = config.DATABASE_PASSWORD


class DataBase:
    def __init__(self):
        self._client = pymongo.MongoClient(
            f"mongodb+srv://{username}:{password}@share-bot.pqplb.mongodb.net/myFirstDatabase?retryWrites=true"
            f"&w=majority")
        self._database = self._client.get_database("Database")
        self.users = self._database.get_collection("users")
        self.purchases = self._database.get_collection("purchases")

    # Methods to work with users

    def add_user(self, user: User):
        self.users.insert_one(vars(user))

    def find_user_by_telegram_id(self, user_id: int) -> dict:
        try:
            return self.users.find_one({"user_id": user_id}, {"username": True, "first_name": True, "last_name": True})
        except AttributeError:
            return dict()

    # ------------------------------------------------------------------------------------------
    # Methods to work with user cards

    def add_user_card(self, user_id: int, card: int, bank: str = None):
        self.users.update_one({"user_id": user_id}, {"$set": {"cards." + str(card): bank}})

    def del_user_card(self, user_id: int, card: int):
        self.users.update_one({"user_id": user_id}, {"$unset": {"cards." + str(card): ""}})

    def get_user_cards(self, user_id: int) -> dict:
        try:
            return self.users.find_one({"user_id": user_id}, {"cards": True}).get("cards")
        except AttributeError:
            return dict()

    def get_cards_from_group(self, group_id: int) -> dict[int, dict[int, str]]:
        list_of_users_object_id = self._get_users_with_cards_from_group(group_id)
        list_of_users = dict()
        for user_object_id in list_of_users_object_id:
            user = self.users.find_one({"_id": user_object_id}, {"user_id": True, "cards": True})
            user_id = user["user_id"]
            user_cards = user["cards"]

            list_of_users[user_id] = user_cards

        return list_of_users

    def _get_users_with_cards_from_group(self, group_id: int) -> list[int]:
        list_of_users_in_group = []
        for user in self.users.find({"cards": {"$ne": {}}}, {"_id": True, "user_id": True}):
            user_id = user["user_id"]
            user_object_id = user["_id"]
            if loader.bot.get_chat_member(chat_id=group_id, user_id=user_id):
                list_of_users_in_group.append(user_object_id)

        return list_of_users_in_group

    # ------------------------------------------------------------------------------------------
    # Methods to work with purchases

    def add_purchase(self, title: str, amount: int) -> str:
        purchase = Purchase(title, amount)
        return str(self.purchases.insert_one(vars(purchase)).inserted_id)

    def delete_purchase(self, purchase_id: str):
        self.purchases.delete_one({"_id": ObjectId(purchase_id)})

    def check_if_user_joined_as_payer(self, user_id: int, purchase_id: str) -> bool:
        list_of_payers = self.purchases.find_one({"_id": ObjectId(purchase_id)}, {"payers": True})["payers"]
        if list_of_payers is None:
            return False
        else:
            return user_id in list_of_payers

    def check_if_user_joined_as_buyer(self, user_id: int, purchase_id: str) -> bool:
        list_of_buyers = self.purchases.find_one({"_id": ObjectId(purchase_id)})["buyers"]
        if list_of_buyers is None:
            return False
        else:
            return user_id in list_of_buyers

    def join_to_purchase_as_payer(self, user_id: int, purchase_id: str):
        self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$push": {"payers": user_id}})

    def remove_user_as_payer(self, user_id: int, purchase_id: str):
        self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$pull": {"payers": user_id}})

    def join_to_purchase_as_buyer(self, user_id: int, amount_of_money_spent: int, purchase_id: str):
        self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$set": {"buyers." + str(user_id): amount_of_money_spent}})

    def remove_user_as_buyer(self, user_id: int, purchase_id: str):
        self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$unset": {"buyers"+str(user_id): ""}})

    # ------------------------------------------------------------------------------------------
