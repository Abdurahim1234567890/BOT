import random

from aiogram.utils import executor
from config import dp
from handlers import client, callbak, extra, admin, fsm_menu, natification
from database import bot_db
import logging
import asyncio


async def on_startup(_):
    asyncio.create_task(natification.time())
    bot_db.sql_create()

fsm_menu.register_handler_fsmmenu(dp)
client.register_handlers_client(dp)
callbak.register__handlers_callback(dp)

admin.register_handler_admin(dp)
natification.register_hendler_notification(dp)

extra.register_handler_extra(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
