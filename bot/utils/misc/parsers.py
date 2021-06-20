from ..db.User import User
from aiogram.types import Message

import re

# valid_card_template_with_bin = r"(\d{6})\d{10}|(\d{4}( )\d{2})\d{2}( \d{4}){2}"
valid_card_template = r"(\d{4} *){4}"


def make_user_from_msg(msg: Message) -> User:
    user_id = msg.from_user.id
    cards = dict()
    username = msg.from_user.username
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    list_of_purchases = []
    user = User(user_id, cards, username, first_name, last_name, list_of_purchases)
    return user


def get_card_from_text(text: str) -> str:
    if re.match(valid_card_template, text):
        match = re.match(valid_card_template, text)
        card = "".join([c if i % 4 != 0 else c+' ' for i, c in enumerate(list(match.group(0)), start=1)]).rstrip()
        return card
