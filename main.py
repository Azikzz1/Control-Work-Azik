from aiogram import executor
from config import dp
import logging
from handlers import commands, fsm_store, fsm_order


commands.register_commands_handlers(dp)
fsm_store.register_handlers_product(dp)
fsm_order.register_handlers_order(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
