from aiogram import types
from loader import dp, db
from bot.keyboards.inline.PurchasesKeyboards.all_purchases_keyboard import AllPurchasesKeyboard


@dp.message_handler(commands="get_all_purchases")
async def get_all_purchases_from_group(message: types.Message):
    text = "All purchases:"
    keyboard = AllPurchasesKeyboard(message.chat.id).keyboard
    await message.answer(text=text, reply_markup=keyboard)
