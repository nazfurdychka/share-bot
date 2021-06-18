
from aiogram import types


class EditButton:
    def __init__(self):
        edit_button = [types.InlineKeyboardButton(text="Edit cards", callback_data="edit_cards")]
        self.keyboard = types.InlineKeyboardMarkup()
        self.keyboard.add(*edit_button)
