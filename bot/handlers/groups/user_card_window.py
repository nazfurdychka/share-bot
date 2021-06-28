import re

from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from loader import dp, db
from keyboards.inline.CardsButtons.CardList import CardList
from keyboards.inline.CardsButtons.DeleteCard import DeleteCard

from bot.states.form_to_add_a_card import Form
from bot.utils.misc.functions_for_manage_card import edit_button_window
from bot.utils.misc.regex import ADD_CARD, DELETE_CARD, DELETE_CARD_WINDOW, VALID_CARD


@dp.callback_query_handler(filters.Regexp(ADD_CARD))
async def information_about_cards(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split()[1]
    await call.message.edit_text(text="Enter card name and card bank you want to add:")
    await state.update_data(user_id=user_id)
    await Form.card.set()


@dp.message_handler(state=Form.card)
async def information_about_cards(message: types.Message, state: FSMContext):
    match = re.match(VALID_CARD, message.text)
    if match:
        card = match.group(1)
        bank = match.group(3)
        await state.update_data(card=card, bank=bank)
        data = await state.get_data()
        card_number = data["card"].replace(" ", "")

        db.add_user_card(user_id=int(data["user_id"]), card=int(card_number), bank=data["bank"])
        output, keyboard = edit_button_window(chat_id=message.chat.id)
        await message.answer(text="Card list:\n" + output, reply_markup=keyboard, parse_mode="markdown")
    else:
        await message.answer("Sorry, this isn't valid card number")
    await state.finish()


@dp.callback_query_handler(filters.Regexp(DELETE_CARD_WINDOW))
async def information_about_cards(call: types.CallbackQuery):
    keyboard = DeleteCard(user_id=call.data.split()[1]).keyboard
    await call.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(filters.Regexp(DELETE_CARD))
async def information_about_cards(call: types.CallbackQuery):
    user_id, card_name = call.data.split()[1], call.data.split()[2]
    db.del_user_card(user_id=int(user_id), card=int(card_name))
    res, keyboard = edit_button_window(chat_id=call.message.chat.id)
    await call.message.delete()
    await call.message.answer(text="Card list:\n" + res, reply_markup=keyboard, parse_mode="markdown")


@dp.callback_query_handler(text="back_to_users")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = CardList(call.message.chat.id).keyboard
    await call.message.edit_text(text="Whose card(s) to edit:", reply_markup=keyboard)
