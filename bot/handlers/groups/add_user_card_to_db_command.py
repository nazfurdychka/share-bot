import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db

from bot.states.form_to_add_a_card import Form
from bot.utils.db.User import User
from bot.utils.misc.functions_for_manage_card import edit_button_window, add_user_card_to_db
from bot.utils.misc.regex import VALID_CARD


@dp.message_handler(commands="add_card")
async def information_about_cards(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer(text="Enter card number and card bank you want to add (example: XXXX XXXX XXXX XXXX bank name):")
    await state.update_data(user_id=user_id)
    await Form.card.set()


@dp.message_handler(state=Form.card)
async def information_about_cards(message: types.Message, state: FSMContext):
    match = re.match(VALID_CARD, message.text)
    if match:
        user_id, username, last_name, first_name = int(message.from_user.id), message.from_user.username, message.from_user.last_name, message.from_user.first_name
        user_object = User(user_id=user_id, username=username, cards=dict(), last_name=last_name, first_name=first_name, list_of_purchases=dict())
        add_user_card_to_db(card=match.group(1), bank=match.group(3), user_object=user_object, user_id=user_id)

        output, keyboard = edit_button_window(chat_id=message.chat.id)
        await message.answer(text="Card list:\n" + output, reply_markup=keyboard, parse_mode="markdown")
    else:
        await message.answer("Sorry, this isn't a valid card number. Please, check if you wrote everything correctly. Click /add_card to try again")
    await state.finish()
