from aiogram import types
from loader import db


class AllPurchasesKeyboard:
    def __init__(self, group_id: str):
        purchases_ids = db.get_all_purchases_from_group(group_id)
        self.check = 1
        if purchases_ids:
            purchases = [(db.get_purchase(id).get("title"), id) for id in purchases_ids]
            purchases_buttons = [types.InlineKeyboardButton(text=title, callback_data="purchase "+str(id)) for title, id in purchases]
            self.keyboard = types.InlineKeyboardMarkup().add(*purchases_buttons)
        else:
            self.check = 0
