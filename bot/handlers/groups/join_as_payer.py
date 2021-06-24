from aiogram import types, filters
from loader import dp, db
from bot.utils.misc.regex import JOIN_AS_PAYER


@dp.callback_query_handler(filters.Regexp(JOIN_AS_PAYER))
async def information_about_cards(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    user_id = call.from_user.id
    if db.check_if_user_joined_as_payer(user_id=user_id, purchase_id=purchase_id):
        db.remove_user_as_payer(user_id=user_id, purchase_id=purchase_id)
        await call.answer("You have removed yourself from payers list")
        new_text = call.message.text.replace(f"\nPayer: {call.from_user.username}", "")
        await call.message.edit_text(text=new_text)
        await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
    else:
        db.join_to_purchase_as_payer(user_id=user_id, purchase_id=purchase_id)
        await call.answer("You have joined the purchase as a payer")
        await call.message.edit_text(text=call.message.text+'\n'+f"Payer: {call.from_user.username}")
        await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
