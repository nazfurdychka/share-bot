
from aiogram import types
from loader import dp, db
from keyboards.inline.CardsButtons.EditButton import EditButton


@dp.message_handler(commands="manage_cards")
async def information_about_cards(message: types.Message):
    keyboard = EditButton().keyboard
    cards = db.get_cards_from_group(group_id=message.chat.id)
    characters = {"{": "", "}": "", ":": " ", ",": "    ", "(": "", ")": "", "\'": ""}
    cards_list = [str(v) for v in cards.items()]
    res = str()
    for k in cards_list:
        trans_table = k.maketrans(characters)
        c = k.translate(trans_table)
        res += c + "\n"
    await message.answer(text="Card list:\n" + res, reply_markup=keyboard)

