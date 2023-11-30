from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from scripts.rooms import Room
from scripts.game import game_start

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Поиск соперника...")
    player_2 = message.from_user.id
    async with Room("data_bases/bot_db.db") as room:
        room = await room.find()
    if room == None:
        async with Room("data_bases/bot_db.db") as room:
            await room.create(player_2)
    else:
        player_1 = room[0]
        async with Room("data_bases/bot_db.db") as room:
            await room.join(player_2, player_1)
        await message.answer("Cоперник найден.")
        await message.bot.send_message(player_1, "Cоперник найден.")
        await game_start(player_1, player_2, message)
