from aiogram import types

from loader import db, dp
from random import randint


@dp.message_handler(commands="test")
async def test(message: types.Message):
    print("eneterd test")
    card = int(message.text.split()[1])
    bank = message.text.split()[2]
    db.add_user_card(message.from_user.id, card, bank)
    await message.reply("added")


@dp.message_handler(commands="test1")
async def test(message: types.Message):
    print("eneterd test1")
    card = int(message.text.split()[1])
    db.del_user_card(message.from_user.id, card)
    await message.reply("deleted")


@dp.message_handler(commands="test2")
async def test(message: types.Message):
    print("eneterd test2")
    cards = db.get_user_cards(message.from_user.id)
    result = [(card, bank) for card, bank in cards.items()]
    print(result)