import re

from aiogram import types
from loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline.PurchasesKeyboards.PurchaseKeyboard import CreatePurchase
from bot.keyboards.inline.PurchasesKeyboards.AllPurchasesKeyboard import AllPurchasesKeyboard
from bot.states.FormToCreatePurchase import FormToCreatePurchase
from bot.states.FormToAddCard import FormToAddCard
from bot.utils.misc.decorators import check_if_user_is_registered
from bot.utils.misc.additional_functions import edit_button_window, make_purchase_text
from bot.utils.misc.parsers import get_title_and_value_from_text
from bot.utils.misc.REGULAR_EXPRESSIONS import VALID_CARD


@dp.message_handler(commands="manage_cards")
@check_if_user_is_registered
async def information_about_cards(message: types.Message):
    res, keyboard = edit_button_window(chat_id=message.chat.id)
    await message.answer(text="Card list:\n" + res, reply_markup=keyboard, parse_mode="markdown")


@dp.message_handler(commands="add_card")
@check_if_user_is_registered
async def information_about_cards(message: types.Message, state: FSMContext):
    match = re.match(VALID_CARD, message.text.split(maxsplit=1)[1])
    if match:
        card, bank = match.group(1).replace(" ", ""), match.group(3).rstrip()
        db.add_user_card(message.from_user.id, int(card), bank)
        output, keyboard = edit_button_window(chat_id=message.chat.id)
        await message.answer(text="Card list:\n" + output, reply_markup=keyboard, parse_mode="markdown")
        return
    elif not match and len(message.text.split()) != 1:
        await message.answer("Sorry, this isn't a valid card number. Please, check if you wrote everything correctly. Click /add_card to try again")
        return
    else:
        await message.answer(text="Enter card number and card bank you want to add (example: XXXX XXXX XXXX XXXX <bank_name>):")
        await FormToAddCard.card.set()


@dp.message_handler(commands="create_purchase")
@check_if_user_is_registered
async def create_purchase(message: types.Message, state: FSMContext):
    title, value = get_title_and_value_from_text(message.text[17:])
    if title:
        purchase_id = db.add_purchase(title=title, amount=value, group_id=message.chat.id)
        keyboard = CreatePurchase(purchase_id, value, title).keyboard
        message_text = make_purchase_text(purchase_id)
        await message.answer(text=message_text, parse_mode="markdown", reply_markup=keyboard)
    else:
        await FormToCreatePurchase.title.set()
        await message.answer("Enter purchase title:")


@dp.message_handler(commands="get_all_purchases")
@check_if_user_is_registered
async def get_all_purchases_from_group(message: types.Message):
    text = "All purchases:"
    keyboard = AllPurchasesKeyboard(message.chat.id).keyboard
    await message.answer(text=text, reply_markup=keyboard)
