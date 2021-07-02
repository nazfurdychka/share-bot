from aiogram import types

from loader import db, dp
from bot.utils.misc.additional_functions import help_text
from bot.utils.misc.decorators import check_if_user_is_registered


@dp.message_handler(commands="help")
@check_if_user_is_registered
async def bot_help(message: types.Message):
    await message.answer(text=help_text())
