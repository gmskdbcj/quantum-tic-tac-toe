from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext, StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

from keyboards import tic_tac_toe_keyboards

from states.languages import LangStates

from bot import storage

router = Router()


@router.message(Command("test_keyboards"))
async def cmd_test(message: Message, state: FSMContext):
    await message.reply("Start game?", reply_markup=await tic_tac_toe_keyboards.Start())
    await message.reply("Your turn!", reply_markup=await tic_tac_toe_keyboards.Turn())
    await message.reply("Select gate:", reply_markup=await tic_tac_toe_keyboards.Gate())
    await message.reply("Select axis:", reply_markup=await tic_tac_toe_keyboards.Axis())
    await message.reply("The end.", reply_markup=await tic_tac_toe_keyboards.End())


@router.message(Command("my_data"))
async def cmd_test(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.reply(str(user_data))


@router.message(Command("my_state"))
async def cmd_test(message: Message, state: FSMContext):
    user_state = await state.get_state()
    await message.reply(str(user_state))


@router.message(Command("my_id"))
async def cmd_test(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await message.reply(str(user_id))
