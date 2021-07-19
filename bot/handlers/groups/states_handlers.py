from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from bot.keyboards.inline.PurchasesKeyboards.PurchaseKeyboard import CreatePurchase
from bot.states.FormToCreatePurchase import FormToCreatePurchase
from bot.states.FormToAddCard import FormToAddCard
from bot.states.FormToJoinAsBuyer import FormToJoinAsBuyer
from bot.utils.misc.decorators import check_if_user_is_registered
from bot.utils.misc.parsers import get_card_bank_from_text
from bot.utils.misc.additional_functions import edit_button_window, make_purchase_text


@dp.message_handler(state=FormToAddCard.card)
@check_if_user_is_registered
async def enter_card(message: types.Message, state: FSMContext):
    card, bank = get_card_bank_from_text(message.text)
    if card:
        data = await state.get_data()
        user_id = data["telegram_id"]
        db.add_user_card(user_id, card, bank)
        output, keyboard = await edit_button_window(chat_id=message.chat.id)
        await message.answer(text="Card list:\n" + output, parse_mode="markdown", reply_markup=keyboard)
    else:
        await message.answer("Sorry, this isn't a valid card number. Please, check if you wrote everything correctly. Click /add_card to try again")
    await state.finish()


@dp.message_handler(state=FormToCreatePurchase.title)
@check_if_user_is_registered
async def title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text.replace("`", '').replace("/", '').replace("<", '').replace('>', ''))
    await FormToCreatePurchase.next()
    await message.reply("Please, enter the cost of this purchase:")


@dp.message_handler(state=FormToCreatePurchase.cost)
@check_if_user_is_registered
async def cost(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["title"]
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.reply("Wrong value! Try again.")
        return
    purchase_id = db.add_purchase(title=name, amount=amount, group_id=message.chat.id)
    keyboard = CreatePurchase(purchase_id, amount).keyboard
    message_text = make_purchase_text(purchase_id)
    await message.answer(text=message_text, parse_mode="markdown", reply_markup=keyboard)
    await state.finish()


@dp.message_handler(state=FormToJoinAsBuyer.amount_payed)
@check_if_user_is_registered
async def join_as_buyer_enter_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    purchase_id, amount_max = data["purchase_id"], data["amount_max"]
    call: types.CallbackQuery = data["call"]
    purchase = db.get_purchase(purchase_id)
    buyers_sum = sum([x for x, _ in purchase.get("buyers", dict()).values()])
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.reply("Wrong value! Press the button to try again.")
        await state.finish()
        return
    if amount+buyers_sum > amount_max:
        await message.reply(f"That is too much! Cost of the purchase was only {amount_max}. Press the button to try again.\n")
        await state.finish()
        return
    user = (message.from_user.id, message.from_user.full_name)
    db.join_to_purchase_as_buyer(user=user, amount_of_money_spent=amount, purchase_id=purchase_id)
    msg_to_edit: types.Message = data["message"]
    msg_to_edit_text = make_purchase_text(purchase_id)
    # await message.delete()
    await call.answer("You have joined purchase as a buyer")
    await msg_to_edit.edit_text(text=msg_to_edit_text, parse_mode="markdown")
    await msg_to_edit.edit_reply_markup(reply_markup=msg_to_edit.reply_markup)
    await state.finish()
