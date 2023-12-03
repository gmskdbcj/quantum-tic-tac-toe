from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.games_keyboards_classes import *


async def Games():
    builder = InlineKeyboardBuilder()
    builder.button(text="Tic-tac-toe", callback_data=GameCallbackFactory(action="tic_tac_toe"))
    builder.adjust(1)
    return builder.as_markup()