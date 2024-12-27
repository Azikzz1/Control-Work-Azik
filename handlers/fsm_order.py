from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config


class FSMOrder(StatesGroup):
    product_id = State()
    size_1 = State()
    quantity = State()
    contact_info = State()
    submit = State()


async def start_order(message: types.Message):
    await FSMOrder.product_id.set()
    await message.reply("Введите артикул товара, который хотите купить")


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text
    await FSMOrder.next()
    await message.reply("Введите размер товара")


async def load_size_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_1'] = message.text
    await FSMOrder.next()
    await message.reply("Введите количество товара")


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text
    await FSMOrder.next()
    await message.reply("Введите свои контактные данные (номер телефона)")


async def load_contact_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact_info'] = message.text
    await FSMOrder.next()
    await message.reply("Подтвердите заказ (Да/Нет)")


async def submit_order(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == 'да':
            await message.reply("Ваш заказ принят!")
            for staff_id in config.staff:
                await config.bot.send_message(staff_id, f"Новый заказ:\nАртикул: {data['product_id']}\n"
                                                 f"Размер: {data['size_1']}\n"
                                                 f"Количество: {data['quantity']}\n"
                                                 f"Контактные данные: {data['contact_info']}")
        else:
            await message.reply("Заказ отменен.")
    await state.finish()


def register_handlers_order(dp: Dispatcher):
    dp.register_message_handler(start_order, commands='order', state=None)
    dp.register_message_handler(load_product_id, state=FSMOrder.product_id)
    dp.register_message_handler(load_size_1, state=FSMOrder.size_1)
    dp.register_message_handler(load_quantity, state=FSMOrder.quantity)
    dp.register_message_handler(load_contact_info, state=FSMOrder.contact_info)
    dp.register_message_handler(submit_order, state=FSMOrder.submit)
