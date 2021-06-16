
from aiogram import types
from loader import dp
from keyboards.inline.CardsButtons import EditButton


@dp.message_handler(commands="cards")
async def information_about_cards(message: types.Message):
    keyboard = EditButton.EditButton().keyboard
    await message.answer("List of cards:", reply_markup=keyboard)
