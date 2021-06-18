
from aiogram import types


class UserSCard:
    def __init__(self):
        manage_card_buttons = [
            types.InlineKeyboardButton(text="Add card", callback_data="add_card"),
            types.InlineKeyboardButton(text="Delete card", callback_data="delete_card"),
            types.InlineKeyboardButton(text="Back to users", callback_data="back_to_users")
        ]
        self.keyboard = types.InlineKeyboardMarkup()
        self.keyboard.add(*manage_card_buttons)
