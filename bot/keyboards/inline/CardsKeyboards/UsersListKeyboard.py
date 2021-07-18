from aiogram import types

from bot.loader import db


class UsersListKeyboard:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    async def get_keyboard(self):
        users = await self._get_users(self.chat_id)
        user_buttons = [
                           types.InlineKeyboardButton(text=full_name, callback_data="manage_cards " + str(
                               telegram_id) + " " + full_name) for full_name, telegram_id in users
                       ] + [types.InlineKeyboardButton(text="Back to cards", callback_data="back_to_cards")]
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*user_buttons)
        return keyboard

    async def _get_users(self, chat_id):
        users = await db.get_user_name_from_group(group_id=chat_id)
        return users
