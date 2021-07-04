from aiogram import types

from loader import db, dp
from bot.utils.misc.decorators import check_if_user_is_registered


@dp.message_handler(commands="start")
@check_if_user_is_registered
async def bot_start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}, I'm Sharebot and I can help you to distribute your money when your buy something with somebody.")
