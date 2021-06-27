
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from loader import dp, db
from keyboards.inline.CardsButtons.CardList import CardList
from keyboards.inline.CardsButtons.DeleteCard import DeleteCard

from bot.keyboards.inline.CardsButtons.EditButton import EditButton
from bot.states.form_to_add_a_card import Form
from bot.utils.misc.regex import ADD_CARD, DELETE_CARD, DELETE_CARD_WINDOW


@dp.callback_query_handler(filters.Regexp(ADD_CARD))    #  text="add_card") # states
async def information_about_cards(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split()[1]
    await call.message.edit_text(text="Enter card name and card bank you want to add:")
    await state.update_data(user_id=user_id)
    await Form.card.set()
    #
    # await call.message.answer("added")


@dp.message_handler(state=Form.card)  # states
async def information_about_cards(message: types.Message, state: FSMContext):
    await state.update_data(card=message.text.split()[0], bank=message.text.split()[1])
    # await state.update_data(amount=int(message.text))
    data = await state.get_data()
    print(data["user_id"], data["card"], data["bank"])
    db.add_user_card(user_id=int(data["user_id"]), card=int(data["card"]), bank=data["bank"])
    keyboard = EditButton( ).keyboard
    cards = db.get_cards_from_group(group_id=message.chat.id)
    characters = {"{": "", "}": "", ":": " ", ",": "    ", "(": "", ")": "", "\'": ""}
    cards_list = [str(v) for v in cards.items()]
    res = str()
    for k in cards_list:
        trans_table = k.maketrans(characters)
        c = k.translate(trans_table)
        res += c + "\n"
    await message.answer(text="Card list:\n" + res, reply_markup=keyboard)

    await state.finish()


@dp.callback_query_handler(filters.Regexp(DELETE_CARD_WINDOW))
async def information_about_cards(call: types.CallbackQuery):
    keyboard = DeleteCard(user_id=call.data.split()[1]).keyboard
    await call.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(filters.Regexp(DELETE_CARD))
async def information_about_cards(call: types.CallbackQuery):
    user_id, card_name = call.data.split()[1], call.data.split()[2]
    db.del_user_card(user_id=int(user_id), card=int(card_name))
    await call.message.answer("deleted")


@dp.callback_query_handler(text="back_to_users")
async def information_about_cards(call: types.CallbackQuery):
    keyboard = CardList(call.message.chat.id).keyboard
    await call.message.edit_text(text="Whose card(s) to edit:", reply_markup=keyboard)
