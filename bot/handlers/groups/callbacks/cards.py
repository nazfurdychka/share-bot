from aiogram import types
from loader import dp, db
from aiogram.dispatcher import filters, FSMContext

from bot.keyboards.inline.CardsKeyboards.UsersListKeyboard import UsersListKeyboard
from bot.keyboards.inline.CardsKeyboards.DeleteCardKeyboard import DeleteCard
from bot.states.FormToAddCard import FormToAddCard
from bot.utils.misc.decorators import check_if_user_is_registered
from bot.utils.misc.additional_functions import edit_button_window, user_cards_window
from bot.utils.misc.REGULAR_EXPRESSIONS import ADD_CARD, MANAGE_CARDS, DELETE_CARD_WINDOW, DELETE_CARD


@check_if_user_is_registered
@dp.callback_query_handler(filters.Regexp(ADD_CARD), state='*')
async def add_card_button(call: types.CallbackQuery, state: FSMContext):
    if len(call.data.split()) == 2:
        user_id = call.data.split()[1]
    else:
        user_id = call.from_user.id
    await call.message.answer(text=f"{call.from_user.full_name}, enter card number and card bank you want to add (example: XXXX XXXX XXXX XXXX bank name):")
    await state.update_data(telegram_id=int(user_id), message=call.message)
    await FormToAddCard.card.set()


@dp.callback_query_handler(text="edit_cards", state='*')
@check_if_user_is_registered
async def edit_cards_button(call: types.CallbackQuery):
    keyboard = UsersListKeyboard(call.message.chat.id).keyboard
    await call.message.edit_text(text="Whose card(s) to edit:", reply_markup=keyboard)


@dp.callback_query_handler(text="back_to_cards", state='*')
@check_if_user_is_registered
async def back_to_cards_button(call: types.CallbackQuery):
    output, keyboard = edit_button_window(chat_id=call.message.chat.id)
    await call.message.edit_text(text="Card list:\n" + output, reply_markup=keyboard, parse_mode="markdown")


@dp.callback_query_handler(filters.Regexp(MANAGE_CARDS), state='*')
@check_if_user_is_registered
async def manage_user_cards_button(call: types.CallbackQuery):
    user_id, user_name = call.data.split()[1], call.data.split(maxsplit=2)[2]
    output, keyboard = user_cards_window(user_id, user_name)
    await call.message.edit_text(text=output, reply_markup=keyboard, parse_mode="markdown")


@dp.callback_query_handler(filters.Regexp(DELETE_CARD_WINDOW), state='*')
@check_if_user_is_registered
async def open_delete_window_button(call: types.CallbackQuery):
    keyboard = DeleteCard(user_id=call.data.split()[1]).keyboard
    await call.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(filters.Regexp(DELETE_CARD), state='*')
@check_if_user_is_registered
async def delete_user_card_button(call: types.CallbackQuery):
    user_id, card_name = call.data.split()[1], call.data.split()[2]
    db.del_user_card(telegram_id=int(user_id), card=card_name)
    res, keyboard = edit_button_window(chat_id=call.message.chat.id)
    await call.message.delete()
    await call.message.answer(text="Card list:\n" + res, reply_markup=keyboard, parse_mode="markdown")


@dp.callback_query_handler(text="back_to_users", state='*')
@check_if_user_is_registered
async def information_about_cards(call: types.CallbackQuery):
    keyboard = UsersListKeyboard(call.message.chat.id).keyboard
    await call.message.edit_text(text="Whose card(s) to edit:", reply_markup=keyboard)
