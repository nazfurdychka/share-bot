
from aiogram import types
from aiogram.dispatcher import filters
from loader import dp, db

from bot.utils.misc.other import calculate
from bot.utils.misc.regex import CALCULATE


@dp.callback_query_handler(filters.Regexp(CALCULATE))
async def information_about_cards(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    b = db.get_all_buyers(purchase_id=purchase_id)
    p = db.get_all_payers(purchase_id=purchase_id)
    a = db.get_purchase_amount(purchase_id=purchase_id)
    output = calculate(buyers=b, payers=p, amount=a)
    await call.message.edit_text(text=output, parse_mode="markdown")
    await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
