
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from loader import dp, db

from bot.keyboards.inline.CardsButtons.CardList import CardList
from bot.keyboards.inline.CardsButtons.EditButton import EditButton
from bot.keyboards.inline.CardsButtons.UserCard import UserSCard
from bot.utils.misc.regex import MANAGE_CARDS


@dp.callback_query_handler(text="back_to_cards")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = EditButton().keyboard
    cards = db.get_cards_from_group(group_id=call.message.chat.id)
    characters = {"{": " ", "}": "", ":": " ", ",": "    ", "(": "", ")": "", "\'": ""}
    cards_list = [str(v) for v in cards.items()]
    res = str()
    for k in cards_list:
        trans_table = k.maketrans(characters)
        c = k.translate(trans_table)
        res += c + "\n"
    await call.message.edit_text(text="Card list:\n" + res)
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(filters.Regexp(MANAGE_CARDS))
async def information_about_cards(call: types.CallbackQuery):
    keyboard = UserSCard().keyboard
    await call.message.edit_text(text="Username and list")
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(text="edit_cards")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = CardList(call.message.chat.id).keyboard
    await call.message.edit_text(text="Whose card(s) to edit:")
    await call.message.edit_reply_markup(reply_markup=keyboard)
