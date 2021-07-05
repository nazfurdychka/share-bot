from ..db.User import User
from aiogram.types import Message

import re
from .REGULAR_EXPRESSIONS import VALID_CARD, VALUE_AND_TITLE


def make_user_from_msg(msg: Message) -> User:
    user_id = msg.from_user.id
    cards = dict()
    username = msg.from_user.username
    full_name = msg.from_user.full_name
    list_of_purchases = []
    user = User(user_id, cards, username, full_name, list_of_purchases)
    return user


def get_card_from_text(text: str) -> str:
    match = re.match(VALID_CARD, text)
    if match:
        card = "".join([c if i % 4 != 0 else c+' ' for i, c in enumerate(list(match.group(0)), start=1)]).rstrip()
        return card


def get_card_bank_from_text(text: str) -> tuple[str, str]:
    match = re.match(VALID_CARD, text)
    if match:
        card, bank = str(match.group(1).replace(" ", "")), str(match.group(3).replace("/", "").replace("`", "").rstrip())
    else:
        card, bank = None, None
    return card, bank


def get_value_and_title_from_text(text: str):
    match = re.match(VALUE_AND_TITLE, text)
    if match:
        value = float(match.group(1))
        title = match.group(2)
        return title, value
    else:
        return None, None


def get_buyers_payers_amount_from_purchase(purchase: dict):
    buyers_db = purchase.get("buyers", dict())
    buyers = dict()
    i = 1
    for value, key in buyers_db.values():
        if buyers.get(key, 0):
            key += f" {str(i)}"
            i += 1
        buyers[key] = value
    payers = [x for _, x in purchase.get("payers", [])]
    amount = purchase["amount"]
    return buyers, payers, amount
