from aiogram import types
from loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline.PurchasesKeyboards.PurchaseKeyboard import CreatePurchase
from bot.keyboards.inline.PurchasesKeyboards.AllPurchasesKeyboard import AllPurchasesKeyboard
from bot.states.FormToCreatePurchase import FormToCreatePurchase
from bot.states.FormToAddCard import FormToAddCard
from bot.utils.misc.decorators import check_if_user_is_registered, check_if_chat_is_group
from bot.utils.misc.additional_functions import edit_button_window, make_purchase_text
from bot.utils.misc.parsers import get_value_and_title_from_text, get_card_bank_from_text


@dp.message_handler(commands="manage_cards")
@check_if_user_is_registered
@check_if_chat_is_group
async def manage_cards(message: types.Message):
    res, keyboard = await edit_button_window(chat_id=message.chat.id)
    await message.answer(text="Card list:\n" + res, reply_markup=keyboard, parse_mode="markdown")


@dp.message_handler(commands="add_card")
@check_if_user_is_registered
@check_if_chat_is_group
async def add_card(message: types.Message, state: FSMContext):
    if len(message.text.split()) == 1:
        await message.answer(text="Enter card number and card bank you want to add (example: XXXX XXXX XXXX XXXX \'bank_name\'):")
        await state.update_data(telegram_id=message.from_user.id)
        await FormToAddCard.card.set()
        return
    else:
        card, bank = get_card_bank_from_text(message.text[10:])
        if card:
            db.add_user_card(message.from_user.id, card, bank)
            output, keyboard = await edit_button_window(chat_id=message.chat.id)
            await message.answer(text="Card list:\n" + output, reply_markup=keyboard, parse_mode="markdown")
            return
        else:
            await message.answer("Sorry, this isn't a valid card number. Please, check if you wrote everything correctly. Click /add_card to try again")
            return


@dp.message_handler(commands="create_purchase")
@check_if_user_is_registered
@check_if_chat_is_group
async def create_purchase(message: types.Message, state: FSMContext):
    title, value = get_value_and_title_from_text(message.text.lstrip("/create_purchase "))
    if title:
        purchase_id = db.add_purchase(title=title, amount=value, group_id=message.chat.id)
        keyboard = CreatePurchase(purchase_id, value).keyboard
        message_text = make_purchase_text(purchase_id)
        await message.answer(text=message_text, parse_mode="markdown", reply_markup=keyboard)
    else:
        await FormToCreatePurchase.title.set()
        await message.answer("Enter purchase title:")


@dp.message_handler(commands="get_all_purchases")
@check_if_user_is_registered
@check_if_chat_is_group
async def get_all_purchases_from_group(message: types.Message):
    text = "All purchases:"
    all_purchases = AllPurchasesKeyboard(message.chat.id)
    if all_purchases.check:
        keyboard = AllPurchasesKeyboard(message.chat.id).keyboard
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(text="No purchases in this group")
