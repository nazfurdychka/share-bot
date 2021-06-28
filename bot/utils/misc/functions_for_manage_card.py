
from loader import db
from keyboards.inline.CardsButtons.EditButton import EditButton

from bot.keyboards.inline.CardsButtons.UserCard import UserSCard


def edit_button_window(chat_id: int):
    keyboard = EditButton().keyboard
    cards = db.get_cards_from_group(group_id=chat_id)
    res = str()
    for k in cards.keys():
        res += "\t\t\t" + k + ": \n"
        for key in cards[k].keys():
            res += "\t\t\t\t\t\t" + "`" + key + "`" + " " + cards[k][key] + "\n"
    return res, keyboard


def user_cards_window(user_id: str, user_name: str):
    keyboard = UserSCard(user_id).keyboard
    user_cards = db.get_user_cards(user_id=int(user_id))
    check = "card" if len(user_cards.keys()) == 1 else "cards"
    res = user_name.replace(", ", " ") + " " + check + ": \n"
    for card, bank in user_cards.items():
        res += "\t\t\t `" + card + "` " + bank + "\n"
    return res, keyboard
