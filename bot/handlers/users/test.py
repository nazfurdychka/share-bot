from aiogram import types

from loader import db, dp


@dp.message_handler(commands="test")
async def test(message: types.Message):
    print("entered test")
    card = int(message.text.split()[1])
    bank = message.text.split()[2]
    db.add_user_card(message.from_user.id, card, bank)
    await message.reply("added")


@dp.message_handler(commands="test1")
async def test(message: types.Message):
    print("entered test1")
    card = int(message.text.split()[1])
    db.del_user_card(message.from_user.id, card)
    await message.reply("deleted")


@dp.message_handler(commands="test2")
async def test(message: types.Message):
    print("entered test2")
    cards = db.get_user_cards(message.from_user.id)
    result = [(card, bank) for card, bank in cards.items()]
    await message.answer(result)


@dp.message_handler(commands="test3")
async def test(message: types.Message):
    print("entered test 3")
    cards = db.get_cards_from_group(message.chat.id)
    await message.answer(cards)
