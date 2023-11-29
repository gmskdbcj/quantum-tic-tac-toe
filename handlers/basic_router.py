from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from scripts.rooms import Room

import asyncio

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Поиск соперника...")
    user_id = message.from_user.id
    async with Room("data_bases/bot_db.db") as room:
        opponent = await room.find()
    if opponent == None:
        async with Room("data_bases/bot_db.db") as room:
            await room.create(user_id)
    else:
        async with Room("data_bases/bot_db.db") as room:
            await room.join(user_id, opponent)
        await message.answer("Cоперник найден.")
        await message.bot.send_message(opponent, "Cоперник найден.")
