import aiogram
from aiogram import types
from loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline.CardsButtons.CreatePurchase import CreatePurchase
from bot.states.Form_for_create_purchase import Form
from bot.utils.misc.parsers import get_title_and_value_from_text
# /create_purchase <value> <title>
# /create_purchase


@dp.message_handler(commands="create_purchase")
async def create_purchase(message: types.Message, state: FSMContext):
    title_value = get_title_and_value_from_text(message.text[17:])
    if title_value:
        purchase_id = db.add_purchase(*title_value)
        keyboard = CreatePurchase(str(purchase_id)).keyboard
        text = f"{title_value[0]}\n{title_value[1]}"
        await message.answer(text=text, reply_markup=keyboard)
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
    await state.update_data(cost=int(message.text))
    title_value = await state.get_data()
    value, title = title_value["cost"], title_value["title"]
    purchase_id = db.add_purchase(title=title, amount=int(value))
    keyboard = CreatePurchase(purchase_id).keyboard
    await message.answer(text=f"{title}\n{value}", reply_markup=keyboard)
    await state.finish()

