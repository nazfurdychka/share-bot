from aiogram import types
from loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline.PurchasesKeyboards.CreatePurchase import CreatePurchase
from bot.states.Form_for_create_purchase import Form
from bot.utils.misc.parsers import get_title_and_value_from_text
from bot.utils.misc.other import make_purchase_text
# /create_purchase <value> <title>
# /create_purchase


@dp.message_handler(commands="create_purchase")
async def create_purchase(message: types.Message, state: FSMContext):
    title, value = get_title_and_value_from_text(message.text[17:])
    if title:
        purchase_id = db.add_purchase(title=title, amount=value, group_id=message.chat.id)
        keyboard = CreatePurchase(purchase_id, value, title).keyboard
        message_text = make_purchase_text(purchase_id)
        await message.answer(text=message_text, parse_mode="markdown", reply_markup=keyboard)
    else:
        await Form.title.set()
        await message.answer("Enter purchase title:")


@dp.message_handler(state=Form.title)
async def title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await Form.next()
    await message.reply("Please, enter the cost of this purchase:")


@dp.message_handler(state=Form.cost)
async def cost(message: types.Message, state: FSMContext):
    title = await state.get_data()
    title = title["title"]
    try:
        value = int(message.text)
    except ValueError:
        await message.reply("Wrong value! Try again.")
        return
    purchase_id = db.add_purchase(title=title, amount=value, group_id=message.chat.id)
    keyboard = CreatePurchase(purchase_id, value, title).keyboard
    message_text = make_purchase_text(purchase_id)
    await message.answer(text=message_text, parse_mode="markdown", reply_markup=keyboard)
    await state.finish()

