from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.tic_tac_toe_keyboards_classes import *


async def Gate(Hadamard=True, Pauli_X=True, Pauli_Y=True, Pauli_Z=True, S=True):
    builder = InlineKeyboardBuilder()
    if Hadamard == True:
        builder.button(text="Hadamard", callback_data=GateCallbackFactory(action="hadamard"))
    if Pauli_X == True:
        builder.button(text="Pauli X", callback_data=GateCallbackFactory(action="pauli_x"))
    if Pauli_Y == True:
        builder.button(text="Pauli Y", callback_data=GateCallbackFactory(action="pauli_y"))
    if Pauli_Z == True:
        builder.button(text="Pauli Z", callback_data=GateCallbackFactory(action="pauli_z"))
    if S == True:
        builder.button(text="S gate (√Z)", callback_data=GateCallbackFactory(action="s_gate"))
    builder.adjust(1)
    return builder.as_markup()


async def Turn():
    builder = InlineKeyboardBuilder()
    builder.button(text="Put gate", callback_data=TurnCallbackFactory(action="put_gate"))
    builder.button(text="Change axis", callback_data=TurnCallbackFactory(action="change_axis"))
    builder.adjust(1)
    return builder.as_markup()


async def Start():
    builder = InlineKeyboardBuilder()
    builder.button(text="Start game", callback_data=StartCallbackFactory(action="start_game"))
    builder.button(text="Cancel game", callback_data=StartCallbackFactory(action="cancel_game"))
    builder.adjust(1)
    return builder.as_markup()


async def End():
    builder = InlineKeyboardBuilder()
    builder.button(text="End game", callback_data=EndCallbackFactory(action="end_game"))
    builder.button(text="Take revenge", callback_data=EndCallbackFactory(action="take_revenge"))
    builder.adjust(1)
    return builder.as_markup()


async def Axis():
    builder = InlineKeyboardBuilder()
    builder.button(text="Change to X", callback_data=AxisCallbackFactory(action="axis_x"))
    builder.button(text="Change to Y", callback_data=AxisCallbackFactory(action="axis_y"))
    builder.button(text="Change to Z", callback_data=AxisCallbackFactory(action="axis_z"))
    builder.adjust(1)
    return builder.as_markup()

async def GateToRow(gate: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="Put to 1 row", callback_data=GateToRowCallbackFactory(action=gate, row=0))
    builder.button(text="Put to 2 row", callback_data=GateToRowCallbackFactory(action=gate, row=1))
    builder.button(text="Put to 3 row", callback_data=GateToRowCallbackFactory(action=gate, row=2))
    builder.adjust(1)
    return builder.as_markup()
