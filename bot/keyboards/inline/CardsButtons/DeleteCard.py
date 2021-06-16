
from aiogram import types
from aiogram.utils.callback_data import CallbackData


class DeleteCard:
    def __init__(self):
        self.callback = CallbackData("prefix", "action")
        manage_card_buttons = [
            types.InlineKeyboardButton(text="Card Number", callback_data=self.callback.new(action="card_num_to_delete")),
        ]
        self.keyboard = types.InlineKeyboardMarkup()
        self.keyboard.add(*manage_card_buttons)
