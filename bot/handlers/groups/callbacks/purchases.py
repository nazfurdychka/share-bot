from aiogram.dispatcher import FSMContext
from loader import dp, db
from aiogram import filters, types

from bot.keyboards.inline.PurchasesKeyboards.PurchaseKeyboard import CreatePurchase
from bot.states.FormToJoinAsBuyer import FormToJoinAsBuyer
from bot.utils.misc.decorators import check_if_user_is_registered
from bot.utils.misc.additional_functions import make_purchase_text, calculate, make_calculate_text
from bot.utils.misc.REGULAR_EXPRESSIONS import DELETE_PURCHASE, JOIN_AS_BUYER, JOIN_AS_PAYER, PURCHASE, CALCULATE


@dp.callback_query_handler(filters.Regexp(PURCHASE))
@check_if_user_is_registered
async def show_purchase(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    purchase = db.get_purchase(purchase_id)
    if purchase:
        value, title = purchase["amount"], purchase["title"]
        keyboard = CreatePurchase(purchase_id, value, title).keyboard
        text = make_purchase_text(purchase_id)
        await call.message.answer(text=text, reply_markup=keyboard, parse_mode="markdown")
    else:
        await call.answer("This purchase is unavailable")


@check_if_user_is_registered
@dp.callback_query_handler(filters.Regexp(DELETE_PURCHASE))
async def information_about_cards(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    title = call.data.split(maxsplit=2)[2]
    db.delete_purchase(purchase_id=purchase_id, group_id=call.message.chat.id, title=title)
    await call.answer("Purchase was deleted!")
    await call.message.edit_text(text="Deleted!")


@dp.callback_query_handler(filters.Regexp(JOIN_AS_BUYER))
@check_if_user_is_registered
async def information_about_cards(call: types.CallbackQuery, state: FSMContext):
    purchase_id = call.data.split()[1]
    amount = int(call.data.split()[2])
    if db.check_if_user_joined_as_buyer(telegram_id=call.from_user.id, purchase_id=purchase_id):
        db.remove_user_as_buyer(telegram_id=call.from_user.id, purchase_id=purchase_id)
        message_text = make_purchase_text(purchase_id)
        await call.answer("You have removed yourself from buyers list")
        await call.message.edit_text(text=message_text, parse_mode="markdown")
        await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
    else:
        await state.update_data(purchase_id=purchase_id, message=call.message, amount_max=amount)
        await call.message.answer(text=f"{call.from_user.full_name}, how much did you pay?")
        await FormToJoinAsBuyer.amount_payed.set()


@dp.callback_query_handler(filters.Regexp(JOIN_AS_PAYER))
@check_if_user_is_registered
async def information_about_cards(call: types.CallbackQuery):
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


@dp.callback_query_handler(filters.Regexp(CALCULATE))
async def information_about_cards(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    purchase = db.get_purchase(purchase_id)
    buyers, payers, amount = purchase["buyers"], purchase["payers"], purchase["amount"]
    result = calculate(buyers=buyers, payers=payers, amount=amount)
    output = make_calculate_text(result)
    await call.message.reply(text=output, parse_mode="markdown", reply_markup=call.message.reply_markup)
    # await call.message.edit_text(text=output, parse_mode="markdown")
    # await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
