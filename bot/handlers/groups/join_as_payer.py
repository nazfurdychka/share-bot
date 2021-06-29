from aiogram import types, filters
from loader import dp, db
from bot.utils.misc.regex import JOIN_AS_PAYER
from bot.utils.misc.other import make_purchase_text


@dp.callback_query_handler(filters.Regexp(JOIN_AS_PAYER))
async def information_about_cards(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    user = (call.from_user.id, call.from_user.full_name)
    if db.check_if_user_joined_as_payer(user_id=user, purchase_id=purchase_id):
        db.remove_user_as_payer(user=user, purchase_id=purchase_id)
        await call.answer("You have removed yourself from payers list")
    else:
        db.join_to_purchase_as_payer(user=user, purchase_id=purchase_id)
        await call.answer("You have joined the purchase as a payer")
    msg_text = make_purchase_text(purchase_id)
    await call.message.edit_text(text=msg_text, parse_mode="markdown")
    await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
