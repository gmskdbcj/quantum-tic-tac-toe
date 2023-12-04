from random import randint

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext, StorageKey

from scripts.rooms import Room
from scripts.quantum_calculations import quant
from scripts.graphic import graphic

from keyboards import tic_tac_toe_keyboards
from keyboards.tic_tac_toe_keyboards_classes import *
from keyboards.games_keyboards_classes import *

from states.tic_tac_toe_states import GameStates

from locales import en as string



def generate_tic_tac_toe_router(storage):
    async def is_win(m):
        if m == [1, 1, 1] or m == [-1, -1, -1]:
            return True
        else:
            return False

    async def user_state(user_id, bot_id):
        user_storage_key = StorageKey(bot_id, user_id, user_id)
        state = FSMContext(storage=storage, key=user_storage_key)
        return state

    start_game_state = ["X", [0, 0, 0], [[], [], []], []]

    router = Router()

    @router.callback_query(StateFilter(None), GameCallbackFactory.filter())
    async def callbacks_tic_tac_toe(callback: CallbackQuery, callback_data: GameCallbackFactory, state: FSMContext):
        if callback_data.action == "tic_tac_toe":
            # await callback.message.delete()
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
                await state.update_data(game_state=start_game_state)
                player_1_state = await user_state(player_1, callback.message.bot.id)
                await player_1_state.update_data(playing_with=player_2)
                await player_1_state.update_data(game_state=start_game_state)
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
                    await callback.message.bot.send_message(
                        chat_id=player_1,
                        text=await graphic(*start_game_state)
                    )
                else:
                    await state.set_state(GameStates.choosing_turn)
                    await player_1_state.set_state(GameStates.wait)
                    await callback.message.answer(
                        text=string.your_turn,
                        reply_markup=await tic_tac_toe_keyboards.Turn()
                    )
                    await callback.message.answer(
                        text=await graphic(*start_game_state)
                    )

            await callback.answer()



    @router.callback_query(StateFilter(GameStates.choosing_turn), TurnCallbackFactory.filter())
    async def callbacks_turn(callback: CallbackQuery, callback_data: TurnCallbackFactory, state: FSMContext):
        # await callback.message.delete()

        if callback_data.action == "put_gate":
            await state.set_state(GameStates.choosing_gate)
            await callback.message.answer(
                text=string.select_gate,
                reply_markup=await tic_tac_toe_keyboards.Gate()
            )

        if callback_data.action == "change_axis":
            await state.set_state(GameStates.choosing_axis)
            await callback.message.answer(
                text=string.select_axis,
                reply_markup=await tic_tac_toe_keyboards.Axis()
            )

        await callback.answer()


    @router.callback_query(StateFilter(GameStates.choosing_axis), AxisCallbackFactory.filter())
    async def callbacks_axis(callback: CallbackQuery, callback_data: AxisCallbackFactory, state: FSMContext):
        #await callback.message.delete()

        axis = None
        if callback_data.action == "axis_x":
            axis = "X"

        if callback_data.action == "axis_y":
            axis = "Y"

        if callback_data.action == "axis_z":
            axis = "Z"

        data = await state.get_data()
        other_player_id = data["playing_with"]
        other_player_state = await user_state(other_player_id, callback.message.bot.id)
        game_state = data["game_state"]
        game_state[0] = axis
        game_state[3] = await quant(*game_state)
        if await is_win(game_state[3]):
            await state.clear()
            await other_player_state.clear()
            await callback.message.answer(
                text=string.you_win + f"\n" + (await graphic(*game_state))
            )
            await callback.message.bot.send_message(
                chat_id=other_player_id,
                text=string.your_opponent_win + f"\n" + (await graphic(*game_state))
            )
        else:
            await state.update_data(game_state=game_state)
            await other_player_state.update_data(game_state=game_state)

            await state.set_state(GameStates.wait)
            await other_player_state.set_state(GameStates.choosing_turn)

            await callback.message.answer(text=await graphic(*game_state))
            await callback.message.answer(text=string.opponent_turn)
            game_state[1] = game_state[3]
            game_state[3] = []
            await callback.message.bot.send_message(
                chat_id=other_player_id,
                text=string.your_turn + f"\n" + (await graphic(*game_state)),
                reply_markup=await tic_tac_toe_keyboards.Turn()
            )

        await callback.answer()


    @router.callback_query(StateFilter(GameStates.choosing_gate), GateCallbackFactory.filter())
    async def callbacks_gate(callback: CallbackQuery, callback_data: GateCallbackFactory, state: FSMContext):
        # await callback.message.delete()
        await state.set_state(GameStates.choosing_row)

        await callback.message.answer(
            text=string.select_row,
            reply_markup=await tic_tac_toe_keyboards.GateToRow(callback_data.action)
        )

        await callback.answer()

    @router.callback_query(StateFilter(GameStates.choosing_row), GateToRowCallbackFactory.filter())
    async def callbacks_gate_to_row(callback: CallbackQuery, callback_data: GateToRowCallbackFactory, state: FSMContext):
        # await callback.message.delete()

        data = await state.get_data()
        other_player_id = data["playing_with"]
        other_player_state = await user_state(other_player_id, callback.message.bot.id)
        game_state = data["game_state"]
        game_state[2][callback_data.row].append(callback_data.action)
        game_state[3] = await quant(*game_state)
        if await is_win(game_state[3]):
            await state.clear()
            await other_player_state.clear()
            await callback.message.answer(
                text=string.you_win + f"\n" + (await graphic(*game_state))
            )
            await callback.message.bot.send_message(
                chat_id=other_player_id,
                text=string.your_opponent_win + f"\n" + (await graphic(*game_state))
            )
        else:
            await state.update_data(game_state=game_state)
            await other_player_state.update_data(game_state=game_state)

            await state.set_state(GameStates.wait)
            await other_player_state.set_state(GameStates.choosing_turn)

            await callback.message.answer(text=await graphic(*game_state))
            await callback.message.answer(text=string.opponent_turn)
            game_state[1] = game_state[3]
            game_state[3] = []
            await callback.message.bot.send_message(
                chat_id=other_player_id,
                text=string.your_turn + f"\n" + (await graphic(*game_state)),
                reply_markup=await tic_tac_toe_keyboards.Turn()
            )

        await callback.answer()


    @router.message(Command("test_turn"))
    async def cmd_test_turn(message: Message, state: FSMContext):
        await state.set_state(GameStates.choosing_turn)
        await message.answer(
            text=string.your_turn,
            reply_markup=await tic_tac_toe_keyboards.Turn()
        )
        await message.answer(
            text=await graphic(*start_game_state)
        )



    return router
