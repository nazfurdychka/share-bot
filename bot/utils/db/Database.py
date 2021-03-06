import pytz
from datetime import datetime

import loader
from .User import User
from .Purchase import Purchase
from .. import config

import pymongo
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

    # ------------------------------------------------------------------------------------------
    # Methods to work with users

    def add_user(self, user: User):
        self.users.insert_one(vars(user))

    def find_user_by_telegram_id(self, telegram_id: int) -> dict:
        try:
            return self.users.find_one({"telegram_id": telegram_id}, {"_id": True})
        except AttributeError:
            return dict()

    # ------------------------------------------------------------------------------------------
    # Methods to work with user cards

    def add_user_card(self, telegram_id: int, card: str, bank: str = ''):
        self.users.update_one({"telegram_id": telegram_id}, {"$set": {"cards." + str(card): bank}})

    def del_user_card(self, telegram_id: int, card: str):
        self.users.update_one({"telegram_id": telegram_id}, {"$unset": {"cards." + str(card): ""}})

    def get_user_cards(self, telegram_id: int) -> dict:
        try:
            return self.users.find_one({"telegram_id": telegram_id}, {"cards": True}).get("cards")
        except AttributeError:
            return dict()

    async def get_cards_from_group(self, group_id: int):  # -> Dict[str, Dict[int, str]]:
        _, full_names, telegram_ids, cards = await self._get_users_with_cards_from_group(group_id)
        list_of_users = dict()
        for full_name, telegram_id, user_cards in zip(full_names, telegram_ids, cards):
            list_of_users[(full_name, telegram_id)] = user_cards
        return list_of_users

    async def _get_users_with_cards_from_group(self, group_id: int):  # -> list[int]:
        object_ids = list()
        full_names = list()
        telegram_ids = list()
        cards = list()
        for user in self.users.find({"cards": {"$ne": {}}}, {"_id": True, "telegram_id": True, "full_name": True, "cards": True}):
            user_telegram_id = user["telegram_id"]
            user_object_id = user["_id"]
            user_full_name = user["full_name"]
            member = await loader.bot.get_chat_member(chat_id=group_id, user_id=user_telegram_id)

            if member["status"] in ("member", "creator", "administrator"):
                user_cards = user["cards"]
                full_names.append(user_full_name)
                object_ids.append(user_object_id)
                telegram_ids.append(user_telegram_id)
                cards.append(user_cards)
        return object_ids, full_names, telegram_ids, cards

    async def get_user_name_from_group(self, group_id: int):
        _, full_names, telegram_ids, _ = await self._get_users_with_cards_from_group(group_id)
        return zip(full_names, telegram_ids)

    # ------------------------------------------------------------------------------------------
    # Methods to work with groups

    def add_new_group(self, group_id, group_title: str):
        tz = "Europe/Kiev"
        timezone = pytz.timezone(tz)
        self.groups.insert_one({
            "group_id": group_id,
            "title": group_title,
            "when_added": datetime.now(tz=timezone).strftime("%d/%m/%Y, %H:%M:%S"),
            "purchases": []}
        )

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

    def add_purchase(self, title: str, amount: float, group_id: int):
        purchase = Purchase(title, amount)
        purchase_id = str(self.purchases.insert_one(vars(purchase)).inserted_id)
        self.groups.update_one({"group_id": group_id}, {"$push": {"purchases": purchase_id}})
        return purchase_id

    def delete_purchase(self, purchase_id: str, group_id: int = None):
        self.purchases.delete_one({"_id": ObjectId(purchase_id)})
        if group_id:
            self.groups.update_one({"group_id": group_id}, {"$pull": {"purchases": purchase_id}})

    def get_purchase(self, purchase_id: str):
        return self.purchases.find_one({"_id": ObjectId(purchase_id)})

    def check_if_user_joined_as_payer(self, user, purchase_id: str) -> bool:
        list_of_payers = self.purchases.find_one({"_id": ObjectId(purchase_id)}, {"payers": True})["payers"]
        return list(user) in list_of_payers

    def check_if_user_joined_as_buyer(self, telegram_id: int, purchase_id: str) -> bool:
        list_of_buyers = self.purchases.find_one({"_id": ObjectId(purchase_id)})["buyers"]
        return str(telegram_id) in list_of_buyers

    def join_to_purchase_as_payer(self, user, purchase_id: str):
        return self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$push": {"payers": user}}).upserted_id

    def remove_user_as_payer(self, user, purchase_id: str):
        return self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$pull": {"payers": user}}).upserted_id

    def join_to_purchase_as_buyer(self, user, amount_of_money_spent: float, purchase_id: str):
        user_id = user[0]
        full_name = user[1]
        return self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$set": {"buyers." + str(user_id): [amount_of_money_spent, full_name]}}).upserted_id

    def remove_user_as_buyer(self, telegram_id: int, purchase_id: str):
        return self.purchases.update_one({"_id": ObjectId(purchase_id)}, {"$unset": {"buyers."+str(telegram_id): ""}}).upserted_id

    # ------------------------------------------------------------------------------------------
