
from aiogram import types
from loader import dp, db
from bot.utils.misc.functions_for_manage_card import edit_button_window


@dp.message_handler(commands="manage_cards")
async def information_about_cards(message: types.Message):
    res, keyboard = edit_button_window(chat_id=message.chat.id)
    await message.answer(text="Card list:\n" + res, reply_markup=keyboard, parse_mode="markdown")

