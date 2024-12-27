from aiogram import types, Dispatcher
from db import main_db
from config import bot


async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Hello {message.from_user.first_name}!\n'
                                f'Твой Telegram ID - {message.from_user.id}')


async def info_handlers(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Я бот, созданный для записи товаров и обработки заказов.\n"
                                "Вы можете использовать меня для управления вашим магазином.")


async def show_products(message: types.Message):
    products = main_db.fetch_all_products()
    if products:
        for product in products:
            caption = (f'Название: {product[1]}\n'
                       f'Категория: {product[2]}\n'
                       f'Размер: {product[3]}\n'
                       f'Стоимость: {product[4]}\n'
                       f'Артикул: {product[5]}\n')
            await message.answer_photo(photo=product[6], caption=caption)
    else:
        await message.reply('Товаров нет')


def register_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(info_handlers, commands=['info'])
    dp.register_message_handler(show_products, commands=['products'])
