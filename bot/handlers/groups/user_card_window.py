
from aiogram import types
from loader import dp, db
from keyboards.inline.CardsButtons.CardList import CardList
from keyboards.inline.CardsButtons.DeleteCard import DeleteCard


@dp.callback_query_handler(text="add_card") # states
async def information_about_cards(call: types.CallbackQuery):
    await call.message.edit_text(text="Enter card you want to add:")
    await call.message.answer("added")


@dp.callback_query_handler(text="delete_card")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = DeleteCard().keyboard
    await call.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(text="back_to_users")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = CardList(call.message.chat.id).keyboard
    await call.message.edit_text(text="Whose card(s) to edit:", reply_markup=keyboard)
