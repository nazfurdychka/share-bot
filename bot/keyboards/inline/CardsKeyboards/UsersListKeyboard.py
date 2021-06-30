from aiogram import types

from bot.loader import db


class UsersListKeyboard:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.users = db.get_user_name_from_group(group_id=chat_id)
        user_buttons = [
            types.InlineKeyboardButton(text=full_name, callback_data="manage_cards " + str(telegram_id) + " " + full_name) for full_name, telegram_id in self.users
        ] + [types.InlineKeyboardButton(text="Back to cards", callback_data="back_to_cards")]
        self.keyboard = types.InlineKeyboardMarkup()
        self.keyboard.add(*user_buttons)
