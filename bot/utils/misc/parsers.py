from ..db.User import User
from aiogram.types import Message


def make_user_from_msg(msg: Message):
    user_id = msg.from_user.id
    card_id = None
    username = msg.from_user.username
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    list_of_purchases = []
    user = User(user_id, card_id, username, first_name, last_name, list_of_purchases)
    return user
