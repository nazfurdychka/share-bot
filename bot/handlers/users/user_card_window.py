
from aiogram import types
from loader import dp
from keyboards.inline.CardsButtons import CardList, DeleteCard


@dp.callback_query_handler(text="add_card")
async def information_about_cards(call: types.CallbackQuery):
    await call.message.edit_text(text="Enter card you want to add:")


@dp.callback_query_handler(text="delete_card")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = DeleteCard.DeleteCard().keyboard
    await call.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(text="back_to_users")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = CardList.CardList().keyboard
    await call.message.edit_reply_markup(keyboard)
