import re

from aiogram import types
from loader import dp
from bot.keyboards.inline.CardsButtons import CardList
from aiogram.dispatcher import filters, FSMContext

from bot.states.form_to_add_a_card import Form
from bot.keyboards.inline.CardsButtons.CardList import CardList
from bot.utils.db.User import User
from bot.utils.misc.functions_for_manage_card import edit_button_window, user_cards_window, add_user_card_to_db
from bot.utils.misc.regex import MANAGE_CARDS, VALID_CARD


@dp.callback_query_handler(text="back_to_cards")
async def information_about_cards(call: types.CallbackQuery):
    output, keyboard = edit_button_window(chat_id=call.message.chat.id)
    await call.message.edit_text(text="Card list:\n" + output, reply_markup=keyboard, parse_mode="markdown")


@dp.callback_query_handler(filters.Regexp(MANAGE_CARDS))
async def information_about_cards(call: types.CallbackQuery):
    user_id, user_name = call.data.split()[1], str(call.data.split()[2:]).replace("\'", "")
    output, keyboard = user_cards_window(user_id, user_name)
    await call.message.edit_text(text=output, reply_markup=keyboard, parse_mode="markdown")


@dp.callback_query_handler(text="add_user_card_to_db")
async def information_about_cards(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await call.message.edit_text(text="Enter card number and card bank you want to add (example: XXXX XXXX XXXX XXXX bank name):")
    await state.update_data(user_id=user_id)
    await Form.card.set()


@dp.message_handler(state=Form.card)
async def information_about_cards(message: types.Message, state: FSMContext):
    match = re.match(VALID_CARD, message.text)
    if match:
        user_id, username, full_name = int(message.from_user.id), message.from_user.full_name, message.from_user.first_name
        user_object = User(user_id=user_id, username=username, cards=dict(), full_name=full_name, list_of_purchases=list())
        add_user_card_to_db(card=match.group(1), bank=match.group(3), user_object=user_object, user_id=user_id)

        output, keyboard = edit_button_window(chat_id=message.chat.id)
        await message.answer(text="Card list:\n" + output, reply_markup=keyboard, parse_mode="markdown")
    else:
        await message.answer("Sorry, this isn't a valid card number. Please, check if you wrote everything correctly. Click /add_card to try again")
    await state.finish()


@dp.callback_query_handler(text="edit_cards")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = CardList(call.message.chat.id).keyboard
    await call.message.edit_text(text="Whose card(s) to edit:", reply_markup=keyboard)
