
from aiogram import types


class EditButton:
    edit_button = [
        types.InlineKeyboardButton(text="Edit cards", callback_data="edit_cards"),
        types.InlineKeyboardButton(text="Add yourself", callback_data="add_user_card_to_db")
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*edit_button)
