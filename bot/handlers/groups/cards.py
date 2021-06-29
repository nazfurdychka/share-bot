
from aiogram import types
from loader import dp
from keyboards.inline.CardsButtons import EditButton
from bot.utils.misc.decorators import check_if_user_is_registered


@dp.message_handler(commands="manage_cards")
@check_if_user_is_registered
async def information_about_cards(message: types.Message):
    keyboard = EditButton.EditButton().keyboard
    await message.answer("List of cards:", reply_markup=keyboard)
