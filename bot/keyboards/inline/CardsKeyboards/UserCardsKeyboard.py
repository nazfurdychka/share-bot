from aiogram import types


class UserCard:
    def __init__(self, user_id):
        self.user_id = user_id
        manage_card_buttons = [
            types.InlineKeyboardButton(text="Add card", callback_data="add_card " + self.user_id),
            types.InlineKeyboardButton(text="Delete card", callback_data="delete_card_window " + self.user_id),
            types.InlineKeyboardButton(text="Back to users", callback_data="back_to_users")
        ]
        self.keyboard = types.InlineKeyboardMarkup()
        self.keyboard.add(*manage_card_buttons)
