
from aiogram import types

from bot.loader import db


class CardList:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.user_list = db.get_user_name_from_group(group_id=chat_id)
        users_list = [
            types.InlineKeyboardButton(text=user, callback_data="manage_cards" + user) for user, user_id in self.user_list
            ] + [types.InlineKeyboardButton(text="Back to cards", callback_data="back_to_cards")]
        self.keyboard = types.InlineKeyboardMarkup()
        self.keyboard.add(*users_list)
