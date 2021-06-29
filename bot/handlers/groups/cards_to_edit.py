
from aiogram import types
from loader import dp
from bot.keyboards.inline.CardsButtons import CardList, EditButton, UserCard


@dp.callback_query_handler(text="edit_cards")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = CardList.CardList().keyboard
    await call.message.edit_text(text="Whose card(s) to edit:")
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(text="back_to_cards")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = EditButton.EditButton().keyboard
    await call.message.edit_text(text="List of cards:")
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(text="manage_cards")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = UserCard.UserSCard().keyboard
    await call.message.edit_text(text="Username and list")
    await call.message.edit_reply_markup(reply_markup=keyboard)
