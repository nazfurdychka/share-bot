from aiogram import types, filters
from loader import dp, db
from bot.utils.misc.regex import DELETE_PURCHASE


@dp.callback_query_handler(filters.Regexp(DELETE_PURCHASE))
async def information_about_cards(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    db.delete_purchase(purchase_id=purchase_id)
    await call.answer("Purchase was deleted!")
    await call.message.edit_text(text="Deleted!")
