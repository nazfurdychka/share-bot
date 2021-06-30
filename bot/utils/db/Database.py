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
        self.groups = self._database.get_collection("groups")

    # Methods to work with users

    def add_user(self, user: User):
        self.users.insert_one(vars(user))

    def find_user_by_telegram_id(self, user_id: int) -> dict:
        try:
            return self.users.find_one({"user_id": user_id}, {"username": True, "full_name": True})
        except AttributeError:
            return dict()

    # ------------------------------------------------------------------------------------------
    # Methods to work with user_id cards

    def add_user_card(self, user_id: int, card: int, bank: str = None):
        self.users.update_one({"user_id": user_id}, {"$set": {"cards." + str(card): bank}})

    def del_user_card(self, user_id: int, card: int):
        self.users.update_one({"user_id": user_id}, {"$unset": {"cards." + str(card): ""}})

    def get_user_cards(self, user_id: int) -> dict:
        try:
            return self.users.find_one({"user_id": user_id}, {"cards": True}).get("cards")
        except AttributeError:
            return dict()

    def get_cards_from_group(self, group_id: int): # -> Dict[int, Dict[int, str]]:
        list_of_users_object_id = (self._get_users_with_cards_from_group(group_id))[0]
        list_of_user_user_full_names = (self._get_users_with_cards_from_group(group_id))[1]
        list_of_users = dict()
        for i, user_object_id in enumerate(list_of_users_object_id):
            user = self.users.find_one({"_id": user_object_id}, {"user_id": True, "cards": True})
            user_info = list_of_user_user_full_names[i]
            user_cards = user["cards"]
            list_of_users[user_info] = user_cards
        return list_of_users

    def _get_users_with_cards_from_group(self, group_id: int):  # -> list[int]:
        list_of_users_in_group = list()
        user_object_user = list()
        list_of_users_id = list()
        for user in self.users.find({"cards": {"$ne": {}}}, {"_id": True, "user_id": True, "first_name": True,
                                                             "last_name": True, "full_name": True}):
            user_id = user["user_id"]
            user_object_id = user["_id"]
            user_last_name = user["last_name"]
            user_first_name = user["first_name"]

            if loader.bot.get_chat_member(chat_id=group_id, user_id=user_id):
                user_object_user.append(str(user_first_name) + " " + str(user_last_name))
                list_of_users_in_group.append(user_object_id)
                list_of_users_id.append(user_id)
        return [list_of_users_in_group, user_object_user, list_of_users_id]

    def get_user_name_from_group(self, group_id: int):
        names = self._get_users_with_cards_from_group(group_id)[1]
        ids = self._get_users_with_cards_from_group(group_id)[2]
        k = list(zip(names, ids))
        return k

 # ------------------------------------------------------------------------------------------
    # Methods to work with groups

    def add_new_group(self, group_id, group_title: str):
        self.groups.insert_one({"group_id": group_id, "title": group_title, "purchases": []})

    def delete_group(self, group_id: str):
        purchases = self.groups.find_one({"group_id": group_id}, {"purchases": True})["purchases"]
        for _, purchase in purchases:   # purchases: [(purchase_title, purchase_id), ...]
            self.purchases.delete_one({"purchase_id": ObjectId(purchase)})
        self.groups.delete_one({"group_id": group_id})

    def get_all_purchases_from_group(self, group_id: int):
        purchases = self.groups.find_one({"group_id": group_id}, {"purchases": True})["purchases"]
        return purchases

    # ------------------------------------------------------------------------------------------
    # Methods to work with purchases

    def add_purchase(self, title: str, amount: int, group_id: int):
        purchase = Purchase(title, amount)
        purchase_id = str(self.purchases.insert_one(vars(purchase)).inserted_id)
        self.groups.update_one({"group_id": group_id}, {"$push": {"purchases": [title, purchase_id]}})
        return purchase_id

    def delete_purchase(self, purchase_id: str, group_id: int = None, title: str = None):
        self.purchases.delete_one({"_id": ObjectId(purchase_id)})
        if group_id:
            self.groups.update_one({"group_id": group_id}, {"$pull": {"purchases": [title, purchase_id]}})

    def get_purchase(self, purchase_id: str):
        return self.purchases.find_one({"_id": ObjectId(purchase_id)})

    # def get_all_purchases_from_group(self, group_id: int):
    #     purchases = self.groups.find_one({"group_id": group_id}, {"purchases": True})["purchases"]
    #     return purchases

    def check_if_user_joined_as_payer(self, user_id, purchase_id: str) -> bool:
        list_of_payers = self.purchases.find_one({"_id": ObjectId(purchase_id)}, {"payers": True})["payers"]
        return list(user_id) in list_of_payers

    def check_if_user_joined_as_buyer(self, user_id: int, purchase_id: str) -> bool:
        list_of_buyers = self.purchases.find_one({"_id": ObjectId(purchase_id)})["buyers"]
        return str(user_id) in list_of_buyers

    def join_to_purchase_as_payer(self, user, purchase_id: str):
        return self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$push": {"payers": user}}).upserted_id

    def remove_user_as_payer(self, user, purchase_id: str):
        return self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$pull": {"payers": user}}).upserted_id

    def join_to_purchase_as_buyer(self, user, amount_of_money_spent: int, purchase_id: str):
        user_id = user[0]
        full_name = user[1]
        return self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$set": {"buyers." + str(user_id): [amount_of_money_spent, full_name]}}).upserted_id

    def remove_user_as_buyer(self, user_id: int, purchase_id: str):
        return self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$unset": {"buyers."+str(user_id): ""}}).upserted_id

    def get_all_buyers(self, purchase_id: str) -> dict:
        buyers = dict()
        for v in self.purchases.find_one({"_id": ObjectId(purchase_id)})["buyers"].values():
            buyers[v[1]] = v[0]
        return buyers

    def get_all_payers(self, purchase_id: str) -> dict:
        payers = dict()
        for i in self.purchases.find_one({"_id": ObjectId(purchase_id)}, {"payers": True})["payers"]:
            payers[i[1]] = 0
        return payers

    def get_purchase_amount(self, purchase_id: str) -> int:
        return self.purchases.find_one({"_id": ObjectId(purchase_id)}, {"amount": True})["amount"]
    # ------------------------------------------------------------------------------------------
