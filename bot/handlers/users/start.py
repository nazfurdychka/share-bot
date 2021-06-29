from aiogram import types

from loader import db, dp
from bot.utils.db.User import User
from bot.utils.misc.parsers import make_user_from_msg


@dp.message_handler(commands="start")
async def bot_start(message: types.Message):
    await message.answer(message.chat.id)
    # user = make_user_from_msg(message)
    # if not db.find_user_by_telegram_id(user.user_id):
    #     db.add_user(user)
    # await message.answer(f"Hello, {message.from_user.full_name}")
