from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import language_keyboards

from states.languages import LangStates

router = Router()


@router.message(Command("lang"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="select_lang",
        reply_markup=await language_keyboards.choosing_language()
    )
    await state.set_state(LangStates.ru)
