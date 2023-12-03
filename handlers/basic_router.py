from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import games_keyboards

router = Router()


@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: Message):
    await message.answer(text="Hello!",
                         reply_markup=await games_keyboards.Games()
                         )


@router.message(Command("cancel"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Canceled all.")
