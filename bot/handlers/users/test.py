from aiogram import types

from loader import db, dp
from random import randint


@dp.message_handler(commands="test")
async def test(message: types.Message):
    card = randint(100000, 100000000)
    db.add_user_card(message.from_user.id, card, "Mono")
