from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start bot"),
            types.BotCommand("help", "Get info"),
            types.BotCommand("manage_cards", "returns list of all cards in this group"),
            types.BotCommand("get_all_purchases", "returns all purchases from this group"),
            types.BotCommand("create_purchase", "/create_purchase <cost> <title>"),
            types.BotCommand("add_card", "/add_card <r> <bank_name>(optional)"),
        ]
    )
