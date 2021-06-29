from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from bot.states.form_to_join_as_buyer import Form
from bot.utils.misc.regex import JOIN_AS_BUYER
from bot.utils.misc.other import make_purchase_text


@dp.callback_query_handler(filters.Regexp(JOIN_AS_BUYER))
async def information_about_cards(call: types.CallbackQuery, state: FSMContext):
    purchase_id = call.data.split()[1]
    amount = int(call.data.split()[2])
    user = call.from_user.id
    if db.check_if_user_joined_as_buyer(user_id=user, purchase_id=purchase_id):
        db.remove_user_as_buyer(user_id=user, purchase_id=purchase_id)
        message_text = make_purchase_text(purchase_id)
        await call.answer("You have removed yourself from buyers list")
        await call.message.edit_text(text=message_text, parse_mode="markdown")
        await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
    else:
        await state.update_data(purchase_id=purchase_id, message=call.message, amount_max=amount)
        await call.message.answer(text=f"{call.from_user.full_name}, how much did you pay?")
        await Form.amount_payed.set()


@dp.message_handler(state=Form.amount_payed)
async def join_as_buyer_enter_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.reply("Wrong value! Try again.")
        return
    data = await state.get_data()
    purchase_id, amount_max = data["purchase_id"], data["amount_max"]
    if amount > amount_max:
        await message.reply(f"That is too much! Cost of the purchase was only {amount_max}.\n {message.from_user.full_name}, how much did you pay?")
        return
    user = (message.from_user.id, message.from_user.full_name)
    db.join_to_purchase_as_buyer(user=user, amount_of_money_spent=amount, purchase_id=purchase_id)
    msg_to_edit: types.Message = data["message"]
    msg_to_edit_text = make_purchase_text(purchase_id)
    # await message.delete()
    await msg_to_edit.edit_text(text=msg_to_edit_text, parse_mode="markdown")
    await msg_to_edit.edit_reply_markup(reply_markup=msg_to_edit.reply_markup)
    await state.finish()
