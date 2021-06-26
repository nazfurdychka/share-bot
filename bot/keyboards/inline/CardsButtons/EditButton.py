
from aiogram import types


class EditButton:
    edit_button = [types.InlineKeyboardButton(text="Edit cards", callback_data="edit_cards")]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*edit_button)
