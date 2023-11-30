from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from scripts.rooms import Room
from scripts.game import game_start

from keyboards import Keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Finding an opponent...")
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
        await message.answer("An opponent has been found.")
        await message.bot.send_message(player_1, "An opponent has been found.")
        await game_start(player_1, player_2, message)


@router.message(Command("test"))
async def cmd_test(message: Message):
    await message.reply("Start game?", reply_markup=await Keyboard.Start())
    await message.reply("Your turn!", reply_markup=await Keyboard.Turn())
    await message.reply("Select gate:", reply_markup=await Keyboard.Gate())
    await message.reply("Select axis:", reply_markup=await Keyboard.Axis())
    await message.reply("The end.", reply_markup=await Keyboard.End())
