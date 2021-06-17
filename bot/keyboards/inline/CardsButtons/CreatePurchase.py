
from aiogram import types


class CreatePurchase:
    def __init__(self):
        create_purchase_buttons = [types.InlineKeyboardButton(text="Join as buyer", callback_data="join_as_buyer"),
                                   types.InlineKeyboardButton(text="Join as payer", callback_data="join_as_payer"),
                                   types.InlineKeyboardButton(text="calculate", callback_data="calculate"),
                                   types.InlineKeyboardButton(text="delete purchase", callback_data="delete_purchase")]
        self.keyboard = types.InlineKeyboardMarkup()
        self.keyboard.add(*create_purchase_buttons)
