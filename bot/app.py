from aiogram import executor

from loader import dp
import utils, middlewares, filters, handlers

from utils.misc.set_bot_default_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, on_startup=on_startup)
