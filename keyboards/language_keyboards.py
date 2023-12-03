from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


async def choosing_language():
    class Buttons:
        En = InlineKeyboardButton(text="English", callback_data="En")
        Ru = InlineKeyboardButton(text="Русский", callback_data="Ru")

    markup = [[Buttons.En], [Buttons.Ru]]
    return InlineKeyboardBuilder(markup=markup).as_markup()

