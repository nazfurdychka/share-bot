
from aiogram import types
from aiogram.dispatcher import filters
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
    user_id = call.data.split()[1]
    keyboard = UserSCard(user_id=user_id).keyboard
    user_cards = db.get_user_cards(user_id=int(user_id))
    list_of_user_cards = list()
    for k, v in user_cards.items():
        list_of_user_cards.append("{:<8} {:<15}".format(k, v))
    await call.message.edit_text(text="".join(list_of_user_cards))
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(text="edit_cards")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = CardList(call.message.chat.id).keyboard
    await call.message.edit_text(text="Whose card(s) to edit:")
    await call.message.edit_reply_markup(reply_markup=keyboard)
