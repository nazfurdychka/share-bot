from aiogram import types
from loader import dp, db, bot


@dp.my_chat_member_handler()
async def bot_was_added_to_group(message: types.ChatMemberUpdated):
    if message.new_chat_member.user.id == dp.bot.id:
        if message.new_chat_member.status == "left":
            db.delete_group(message.chat.id)
            await dp.bot.send_message(chat_id=395589642, text=f"Bot has been deleted from group {message.chat.full_name}")
        else:
            db.add_new_group(group_id=message.chat.id, group_title=message.chat.title)
            await dp.bot.send_message(chat_id=message.chat.id, text="Hello, I will help you manage your shared expenses. Enter /help for more info.", parse_mode="markdown")
            await dp.bot.send_message(chat_id=395589642, text=f"Bot has been added to group {message.chat.title}")
