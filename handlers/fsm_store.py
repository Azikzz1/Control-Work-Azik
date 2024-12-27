from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import main_db
import config


class FSMProduct(StatesGroup):
    name = State()
    category = State()
    size_1 = State()
    price = State()
    product_id = State()
    photo = State()
    submit = State()


async def add_product_start(message: types.Message):
    if message.from_user.id in config.staff:
        await FSMProduct.name.set()
        await message.reply("Введите название продукта")
    else:
        await message.reply("Извините, у вас нет доступа к этой команде.")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['model_name'] = message.text
    await FSMProduct.next()
    await message.reply("Введите категорию продукта")


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await FSMProduct.next()
    await message.reply("Введите размеры продукта")


async def load_size_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_1'] = message.text
    await FSMProduct.next()
    await message.reply("Введите цену продукта")


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMProduct.next()
    await message.reply("Введите артикул продукта")


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text
    await FSMProduct.next()
    await message.reply("Отправьте фото продукта")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.answer(f'Верные ли данные? (Да/Нет)')
    await message.answer_photo(photo=data['photo'],
                               caption=f'Название модели: - {data["model_name"]}\n'
                                       f'Категория: - {data["category"]}\n'
                                       f'Размер: - {data["size_1"]}\n'
                                       f'Стоимость: - {data["price"]}\n'
                                       f'Артикул: - {data["product_id"]}\n')
    await FSMProduct.submit.set()


async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            await main_db.sql_insert_store_products(
                model_name=data['model_name'],
                category=data['category'],
                size_1=data['size_1'],
                price=data['price'],
                product_id=data['product_id'],
                photo=data['photo']
            )
        await message.answer('Товар успешно добавлен!')
        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer('Добавление товара отменено.')
        await state.finish()
    else:
        await message.answer('Пожалуйста, введите "Да" или "Нет".')


def register_handlers_product(dp: Dispatcher):
    dp.register_message_handler(add_product_start, commands='add_product', state=None)
    dp.register_message_handler(load_name, state=FSMProduct.name)
    dp.register_message_handler(load_category, state=FSMProduct.category)
    dp.register_message_handler(load_size_1, state=FSMProduct.size_1)
    dp.register_message_handler(load_price, state=FSMProduct.price)
    dp.register_message_handler(load_product_id, state=FSMProduct.product_id)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMProduct.photo)
    dp.register_message_handler(load_submit, state=FSMProduct.submit)
