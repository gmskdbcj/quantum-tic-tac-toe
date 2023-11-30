from aiogram.types import Message

async def game_start(player_1: int, player_2: int, message: Message):
    send_message = message.bot.send_message

    await send_message(player_1, "...")
    await send_message(player_2, "...")