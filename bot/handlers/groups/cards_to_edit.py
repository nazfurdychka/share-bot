import re

from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from loader import dp, db

from bot.states.form_to_add_a_card import Form
from bot.keyboards.inline.CardsButtons.CardList import CardList
from bot.utils.db.User import User
from bot.utils.misc.functions_for_manage_card import edit_button_window, user_cards_window
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
    await call.message.edit_text(text="Enter card name and card bank you want to add:")
    await state.update_data(user_id=user_id)
    await Form.card.set()


@dp.message_handler(state=Form.card)
async def information_about_cards(message: types.Message, state: FSMContext):
    match = re.match(VALID_CARD, message.text)
    if match:
        card = match.group(1)
        bank = match.group(3)
        await state.update_data(card=card, bank=bank)  # change
        data = await state.get_data()
        card_number = data["card"].replace(" ", "")

        user_id, username, last_name, first_name = int(
            message.from_user.id), message.from_user.username, message.from_user.last_name, message.from_user.first_name
        user_object = User(user_id=user_id, username=username, cards=dict(), last_name=last_name, first_name=first_name, list_of_purchases=dict())

        if db.find_user_by_telegram_id(user_id=user_id):
            db.add_user_card(user_id=user_id, card=int(card_number), bank=data["bank"])
        else:
            db.add_user(user_object)
            db.add_user_card(user_id=user_id, card=int(card_number), bank=data["bank"])

        output, keyboard = edit_button_window(chat_id=message.chat.id)
        await message.answer(text="Card list:\n" + output, reply_markup=keyboard, parse_mode="markdown")
    else:
        await message.answer("Sorry, this isn't valid card number")
    await state.finish()


@dp.callback_query_handler(text="edit_cards")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = CardList(call.message.chat.id).keyboard
    await call.message.edit_text(text="Whose card(s) to edit:", reply_markup=keyboard)
