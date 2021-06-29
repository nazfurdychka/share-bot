from aiogram import types, filters
from loader import dp, db
from bot.utils.misc.regex import DELETE_PURCHASE


@dp.callback_query_handler(filters.Regexp(DELETE_PURCHASE))
async def information_about_cards(call: types.CallbackQuery):
    purchase_id = call.data.split()[1]
    title = call.data.split(maxsplit=2)[2]
    db.delete_purchase(purchase_id=purchase_id, group_id=call.message.chat.id, title=title)
    await call.answer("Purchase was deleted!")
    await call.message.edit_text(text="Deleted!")
