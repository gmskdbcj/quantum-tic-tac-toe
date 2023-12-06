import asyncio
import logging
from os import mkdir

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext, StorageKey
from aiogram.filters import Command
from aiogram.types import Message

from handlers import basic_router, testing_router, language_router
from handlers.tic_tac_toe_router import generate_tic_tac_toe_router

import json

from pathlib import Path

storage = MemoryStorage()

tic_tac_toe_router = generate_tic_tac_toe_router(storage)

with open('private_config.json', 'r') as file:
    token: str = json.load(file)["BOT_TOKEN"]


logging.basicConfig(level=logging.INFO)


async def main():

    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    dp.include_routers(basic_router.router,
                       tic_tac_toe_router,
                       testing_router.router,
                       language_router.router
                       )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    db_path = Path("data_bases/")
    if not db_path.is_dir():
        mkdir("data_bases")
    db_path = Path("data_bases/bot_db.db")
    if db_path.is_file():
        db_path.unlink()
    asyncio.run(main())
