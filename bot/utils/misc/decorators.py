from aiogram import types
from loader import db
from .parsers import make_user_from_msg


def check_if_user_is_registered(func):
    def wrapper(*args):
        message: types.Message = args[0]
        user_id = message.from_user.id
        if db.find_user_by_telegram_id(user_id=user_id):
            pass
        else:
            user = make_user_from_msg(message)
            db.add_user(user)
        return func(*args)
    return wrapper
