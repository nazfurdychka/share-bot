
from aiogram import types
from loader import dp


@dp.callback_query_handler(text="calculate")
async def information_about_cards(call: types.CallbackQuery):
    await call.message.edit_text(text="Calculate:")
    await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
