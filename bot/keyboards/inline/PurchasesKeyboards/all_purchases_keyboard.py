from aiogram import types
from loader import db


class AllPurchasesKeyboard:
    def __init__(self, group_id: str):
        purchases = db.get_all_purchases_from_group(group_id)
        purchases_buttons = [types.InlineKeyboardButton(text=title, callback_data="purchase "+str(id)) for title, id in purchases]
        self.keyboard = types.InlineKeyboardMarkup().add(*purchases_buttons)
