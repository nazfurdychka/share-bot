from ..db.User import User
from aiogram.types import Message

import re
from .REGULAR_EXPRESSIONS import VALID_CARD, VALUE_AND_TITLE
# valid_card_template_with_bin = r"(\d{6})\d{10}|(\d{4}( )\d{2})\d{2}( \d{4}){2}"


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


def get_title_and_value_from_text(text: str):
    match = re.match(VALUE_AND_TITLE, text)
    if match:
        value = int(match.group(1))
        title = match.group(2)
        return title, value
    else:
        return None, None
