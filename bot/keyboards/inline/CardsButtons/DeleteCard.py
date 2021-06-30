
from aiogram import types
from bot.loader import db


class DeleteCard:
    def __init__(self, user_id):
        self.user_cards = db.get_user_cards(user_id=int(user_id))
        manage_card_buttons = [
            types.InlineKeyboardButton(text=str(card) + " " + str(bank), callback_data="delete_card " + str(user_id) + " " + str(card)) for card, bank in self.user_cards.items()
        ]
        self.keyboard = types.InlineKeyboardMarkup()
        self.keyboard.add(*manage_card_buttons)
