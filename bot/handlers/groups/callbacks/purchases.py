from aiogram.dispatcher import FSMContext
from loader import dp, db
from aiogram import filters, types

from bot.keyboards.inline.PurchasesKeyboards.PurchaseKeyboard import CreatePurchase
from bot.states.FormToJoinAsBuyer import FormToJoinAsBuyer
from bot.utils.misc.decorators import check_if_user_is_registered
from bot.utils.misc.parsers import get_buyers_payers_amount_from_purchase
from bot.utils.misc.additional_functions import make_purchase_text, calculate, make_calculate_text, check_if_purchase_correct
from bot.utils.misc.REGULAR_EXPRESSIONS import DELETE_PURCHASE, JOIN_AS_BUYER, JOIN_AS_PAYER, PURCHASE, CALCULATE


@dp.callback_query_handler(filters.Regexp(PURCHASE), state='*')
@check_if_user_is_registered
async def show_purchase_button(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    purchase = db.get_purchase(purchase_id)
    if purchase:
        value, title = purchase.get("amount"), purchase.get("title")
        keyboard = CreatePurchase(purchase_id, value).keyboard
        text = make_purchase_text(purchase_id)
        await call.message.answer(text=text, reply_markup=keyboard, parse_mode="markdown")
    else:
        await call.answer("This purchase is unavailable")


@check_if_user_is_registered
@dp.callback_query_handler(filters.Regexp(DELETE_PURCHASE), state='*')
async def delete_purchase_button(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    title = db.get_purchase(purchase_id).get("title")
    db.delete_purchase(purchase_id=purchase_id, group_id=call.message.chat.id)
    await call.answer("Purchase was deleted!")
    await call.message.edit_text(text=f"Purchase `{title}` was deleted.", parse_mode="markdown")


@dp.callback_query_handler(filters.Regexp(JOIN_AS_BUYER), state='*')
@check_if_user_is_registered
async def join_as_buyer_button(call: types.CallbackQuery, state: FSMContext):
    purchase_id = call.data.split()[1]
    amount = float(call.data.split()[2])
    if db.check_if_user_joined_as_buyer(telegram_id=call.from_user.id, purchase_id=purchase_id):
        db.remove_user_as_buyer(telegram_id=call.from_user.id, purchase_id=purchase_id)
        message_text = make_purchase_text(purchase_id)
        await call.answer("You have removed yourself from buyers list")
        await call.message.edit_text(text=message_text, parse_mode="markdown")
        await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
    else:
        await state.update_data(purchase_id=purchase_id, message=call.message, amount_max=amount, call=call)
        await call.message.answer(text=f"{call.from_user.full_name}, how much did you pay?")
        await FormToJoinAsBuyer.amount_payed.set()


@dp.callback_query_handler(filters.Regexp(JOIN_AS_PAYER), state='*')
@check_if_user_is_registered
async def join_as_payer_button(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    user = (call.from_user.id, call.from_user.full_name)
    if db.check_if_user_joined_as_payer(user=user, purchase_id=purchase_id):
        db.remove_user_as_payer(user=user, purchase_id=purchase_id)
        await call.answer("You have removed yourself from payers list")
    else:
        db.join_to_purchase_as_payer(user=user, purchase_id=purchase_id)
        await call.answer("You have joined the purchase as a payer")
    msg_text = make_purchase_text(purchase_id)
    await call.message.edit_text(text=msg_text, parse_mode="markdown")
    await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)


@dp.callback_query_handler(filters.Regexp(CALCULATE), state='*')
async def calculate_purchase_button(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    purchase = db.get_purchase(purchase_id)
    error_code, error_message = check_if_purchase_correct(purchase)
    output = error_message
    if error_code == -2:
        pass
    else:
        buyers, payers, amount = get_buyers_payers_amount_from_purchase(purchase)
        result = calculate(buyers=buyers, payers=payers, amount=amount)
        output += make_calculate_text(result)
    await call.message.reply(text=output, parse_mode="markdown")
