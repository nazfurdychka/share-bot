from aiogram import types, filters
from loader import dp, db
from bot.keyboards.inline.PurchasesKeyboards.CreatePurchase import CreatePurchase
from bot.utils.misc.regex import PURCHASE
from bot.utils.misc.other import make_purchase_text


@dp.callback_query_handler(filters.Regexp(PURCHASE))
async def show_purchase(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    purchase = db.get_purchase(purchase_id)
    value, title = purchase["amount"], purchase["title"]
    keyboard = CreatePurchase(purchase_id, value, title).keyboard
    text = make_purchase_text(purchase_id)
    await call.message.answer(text=text, reply_markup=keyboard, parse_mode="markdown")
