
from aiogram import types
from loader import dp

from keyboards.inline.CardsButtons import CreatePurchase


@dp.callback_query_handler(text="join_as_payer")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = CreatePurchase.CreatePurchase().keyboard
    await call.message.edit_text(text="New payers")
    await call.message.edit_reply_markup(reply_markup=keyboard)
