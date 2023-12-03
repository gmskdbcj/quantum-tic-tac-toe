from random import randint

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext, StorageKey

from scripts.rooms import Room
from scripts.game import game_start
from scripts.quantum_calculations import quant
from scripts.graphic import graphic

from keyboards import tic_tac_toe_keyboards
from keyboards.tic_tac_toe_keyboards_classes import *
from keyboards.games_keyboards_classes import *

from states.tic_tac_toe_states import GameStates

from locales import en as string



def generate_tic_tac_toe_router(storage):

    async def user_state(user_id, bot_id):
        user_storage_key = StorageKey(bot_id, user_id, user_id)
        state = FSMContext(storage=storage, key=user_storage_key)
        return state

    router = Router()

    @router.callback_query(StateFilter(None), GameCallbackFactory.filter())
    async def callbacks_turn(callback: CallbackQuery, callback_data: GameCallbackFactory, state: FSMContext):
        if callback_data.action == "tic_tac_toe":
            await callback.message.delete()
            await callback.message.answer("Finding an opponent...")
            player_2 = callback.message.chat.id
            async with Room("data_bases/bot_db.db") as room:
                room_f = await room.find()
                if room_f == None:
                    await room.create(player_2)
                else:
                    player_1 = room_f[0]
                    await room.delete(player_1)
            if room_f != None:
                await state.update_data(playing_with=player_1)
                player_1_state = await user_state(player_1, callback.message.bot.id)
                await player_1_state.update_data(playing_with=player_2)
                await callback.message.answer(text="An opponent has been found.",)
                await callback.message.bot.send_message(
                    chat_id=player_1,
                    text="An opponent has been found.",
                )
                first_turn_player = randint(1, 2)
                if first_turn_player == 1:
                    await player_1_state.set_state(GameStates.choosing_turn)
                    await state.set_state(GameStates.wait)
                    await callback.message.bot.send_message(
                        chat_id=player_1,
                        text=string.your_turn,
                        reply_markup=await tic_tac_toe_keyboards.Turn()
                    )
                else:
                    await state.set_state(GameStates.choosing_turn)
                    await player_1_state.set_state(GameStates.wait)
                    await callback.message.answer(
                        text=string.your_turn,
                        reply_markup=await tic_tac_toe_keyboards.Turn()
                    )



    @router.callback_query(StateFilter(GameStates.choosing_turn), TurnCallbackFactory.filter())
    async def callbacks_turn(callback: CallbackQuery, callback_data: TurnCallbackFactory, state: FSMContext):
        if callback_data.action == "put_gate":
            await callback.message.delete()
            await state.set_state(GameStates.choosing_gate)
            await callback.message.answer(
                text=string.select_gate,
                reply_markup=await tic_tac_toe_keyboards.Gate()
            )
            await callback.answer()

        if callback_data.action == "change_axis":
            await callback.message.delete()
            await state.set_state(GameStates.choosing_axis)
            await callback.message.answer(
                text=string.select_axis,
                reply_markup=await tic_tac_toe_keyboards.Axis()
            )
            await callback.answer()


    @router.callback_query(StateFilter(GameStates.choosing_axis), AxisCallbackFactory.filter())
    async def callbacks_turn(callback: CallbackQuery, callback_data: AxisCallbackFactory, state: FSMContext):
        await callback.message.delete()
        if callback_data.action == "axis_x":
            await callback.message.answer(text="x")

        if callback_data.action == "axis_y":
            await callback.message.answer(text="y")

        if callback_data.action == "axis_z":
            await callback.message.answer(text="z")

        await state.set_state(GameStates.wait)
        await callback.message.answer(text=string.opponent_turn)
        player_data = await state.get_data()
        other_player_id = player_data["playing_with"]
        other_player_state = await user_state(other_player_id, callback.message.bot.id)
        await other_player_state.set_state(GameStates.choosing_turn)
        await callback.message.bot.send_message(
            chat_id=other_player_id,
            text=string.your_turn,
            reply_markup=await tic_tac_toe_keyboards.Turn()
        )
        await callback.answer()


    @router.callback_query(StateFilter(GameStates.choosing_gate), GateCallbackFactory.filter())
    async def callbacks_turn(callback: CallbackQuery, callback_data: GateCallbackFactory, state: FSMContext):
        await callback.message.delete()
        if callback_data.action == "pauli_x":
            await callback.message.answer(text="pauli_x")

        if callback_data.action == "pauli_y":
            await callback.message.answer(text="pauli_y")

        if callback_data.action == "pauli_z":
            await callback.message.answer(text="pauli_z")

        await state.set_state(GameStates.wait)
        await callback.message.answer(text=string.opponent_turn)
        player_data = await state.get_data()
        other_player_id = player_data["playing_with"]
        other_player_state = await user_state(other_player_id, callback.message.bot.id)
        await other_player_state.set_state(GameStates.choosing_turn)
        await callback.message.bot.send_message(
            chat_id=other_player_id,
            text=string.your_turn,
            reply_markup=await tic_tac_toe_keyboards.Turn()
        )
        await callback.answer()



    return router
