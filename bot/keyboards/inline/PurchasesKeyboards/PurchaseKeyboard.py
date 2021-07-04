from aiogram import types


class CreatePurchase:
    def __init__(self, purchase_id: str, value: float, title: str):
        create_purchase_buttons = \
            [
                types.InlineKeyboardButton(text="Join as buyer", callback_data="join_as_buyer " + purchase_id + " " + str(value)),
                types.InlineKeyboardButton(text="Join as payer", callback_data="join_as_payer " + purchase_id),
                types.InlineKeyboardButton(text="calculate", callback_data="calculate " + purchase_id),
                types.InlineKeyboardButton(text="delete purchase", callback_data="delete_purchase " + purchase_id)
            ]
        self.keyboard = types.InlineKeyboardMarkup()
        self.keyboard.add(*create_purchase_buttons)
