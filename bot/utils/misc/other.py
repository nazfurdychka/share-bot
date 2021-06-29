from aiogram import types
from loader import db, bot


def make_purchase_text(purchase_id: str):
    purchase = db.get_purchase(purchase_id)
    text = "`{} - {}`\n".format(purchase["title"], purchase["amount"])
    text += "Buyers:\n"
    for _, buyer_amount in purchase["buyers"].items():
        amount = buyer_amount[0]
        user = buyer_amount[1]
        text += f"`{user} - {amount}`\n"
    text += "Payers:\n"
    for payer in purchase["payers"]:
        user = payer[1]
        text += f"`{user}`"
        text += '\n'
    return text
