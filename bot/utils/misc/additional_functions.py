from loader import db

from bot.keyboards.inline.CardsKeyboards.CardListKeyboard import EditButton
from bot.keyboards.inline.CardsKeyboards.UserCardsKeyboard import UserCard


def edit_button_window(chat_id: int):
    keyboard = EditButton.keyboard
    cards = db.get_cards_from_group(group_id=chat_id)
    res = str()
    for k in cards.keys():
        res += "\t\t\t" + k[0] + ": \n"
        for key in cards[k].keys():
            res += "\t\t\t\t\t\t" + "`" + key + "`" + " " + cards[k][key] + "\n"
    return res, keyboard


def user_cards_window(user_id: str, user_name: str):
    keyboard = UserCard(user_id).keyboard
    user_cards = db.get_user_cards(telegram_id=int(user_id))
    check = "card" if len(user_cards.keys()) == 1 else "cards"
    res = user_name.replace(", ", " ") + " " + check + ": \n"
    for card, bank in user_cards.items():
        res += "\t\t\t `" + card + "` " + bank + "\n"
    return res, keyboard


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
