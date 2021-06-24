from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from bot.states.form_to_join_as_buyer import Form
from bot.utils.misc.regex import JOIN_AS_BUYER


@dp.callback_query_handler(filters.Regexp(JOIN_AS_BUYER))
async def information_about_cards(call: types.CallbackQuery, state: FSMContext):
    purchase_id = call.data.split()[1]
    user_id = call.from_user.id
    if db.check_if_user_joined_as_buyer(user_id=user_id, purchase_id=purchase_id):
        db.remove_user_as_buyer(user_id=user_id, purchase_id=purchase_id)
        await call.answer("You have removed yourself from buyers list")
        await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
    else:
        await Form.amount.set()
        await state.update_data(purchase_id=purchase_id, message=call.message)
        await call.message.answer(text="How much did you pay?")


@dp.message_handler(state=Form.amount)
async def join_as_buyer_enter_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount=int(message.text))
    user_id, username = message.from_user.id, message.from_user.username
    data = await state.get_data()
    purchase_id = data["purchase_id"]
    amount = int(message.text)
    db.join_to_purchase_as_buyer(user_id=user_id, amount_of_money_spent=amount, purchase_id=purchase_id)
    msg_to_edit: types.Message = data["message"]
    msg_to_edit_text = msg_to_edit.text + f"\nBuyer: {username} {amount}"
    # await message.delete()
    await msg_to_edit.edit_text(text=msg_to_edit_text)
    await msg_to_edit.edit_reply_markup(reply_markup=msg_to_edit.reply_markup)
    await state.finish()
