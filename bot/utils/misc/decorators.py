from aiogram import types
from loader import db
from .parsers import make_user_from_msg
from functools import wraps


def check_if_user_is_registered(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        message: types.Message = args[0]
        user_id = message.from_user.id
        if db.find_user_by_telegram_id(telegram_id=user_id):
            pass
        else:
            user = make_user_from_msg(message)
            db.add_user(user)
        return func(*args, **kwargs)
    return wrapper


def check_if_chat_is_group(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        message: types.Message = args[0]
        if message.chat.type == "group":
            return await func(*args, **kwargs)
        else:
            await message.answer("Sorry, but this command created for groups, not for {} chat".format(message.chat.type))
    return wrapper
