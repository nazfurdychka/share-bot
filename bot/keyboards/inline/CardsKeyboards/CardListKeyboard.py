from aiogram import types


class EditButton:
    buttons = [
        types.InlineKeyboardButton(text="Edit cards", callback_data="edit_cards"),
        types.InlineKeyboardButton(text="Add yourself", callback_data="add_card")
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
