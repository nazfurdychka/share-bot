
from aiogram import types
from loader import dp
from aiogram.dispatcher import FSMContext
from keyboards.inline.CardsButtons import CreatePurchase
from states.Form_for_create_purchase import Form


@dp.message_handler(commands="create_purchase")
async def food_chosen(message: types.Message, state: FSMContext):
    await Form.title.set()
    await message.answer("Enter purchase title:")


@dp.message_handler(state=Form.title)
async def title(message: types.Message, state: FSMContext):
    await Form.next()
    await message.reply("Please, enter cost for this purchase:")


@dp.message_handler(state=Form.cost)
async def title(message: types.Message, state: FSMContext):
    keyboard = CreatePurchase.CreatePurchase().keyboard
    await message.answer(text="Title", reply_markup=keyboard)
    await state.finish()
