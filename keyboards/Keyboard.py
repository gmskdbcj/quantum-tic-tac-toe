from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


async def Gate(Hadamard=True, Pauli_X=True, Pauli_Y=True, Pauli_Z=True):
    class Buttons:
        Hadamard = InlineKeyboardButton(text="Hadamard", callback_data="Hadamard")
        Pauli_X = InlineKeyboardButton(text="Pauli X", callback_data="Pauli X")
        Pauli_Y = InlineKeyboardButton(text="Pauli Y", callback_data="Pauli Y")
        Pauli_Z = InlineKeyboardButton(text="Pauli Z", callback_data="Pauli Z")

    markup = []

    if Hadamard == True:
        markup.append([Buttons.Hadamard])
    if Pauli_X == True:
        markup.append([Buttons.Pauli_X])
    if Pauli_Y == True:
        markup.append([Buttons.Pauli_Y])
    if Pauli_Z == True:
        markup.append([Buttons.Pauli_Z])

    return InlineKeyboardBuilder(markup=markup).as_markup()


async def Turn():
    class Buttons:
        Put_gate = InlineKeyboardButton(text="Put gate", callback_data="Put gate")
        Change_axis = InlineKeyboardButton(text="Change axis", callback_data="Change axis")

    markup = [[Buttons.Put_gate], [Buttons.Change_axis]]
    return InlineKeyboardBuilder(markup=markup).as_markup()


async def Start():
    class Buttons:
        Start_game = InlineKeyboardButton(text="Start game", callback_data="Start game")
        Cancel_game = InlineKeyboardButton(text="Cancel game", callback_data="Cancel game")

    markup = [[Buttons.Start_game], [Buttons.Cancel_game]]
    return InlineKeyboardBuilder(markup=markup).as_markup()


async def End():
    class Buttons:
        End_game = InlineKeyboardButton(text="End game", callback_data="End game")
        Take_revenge = InlineKeyboardButton(text="Take revenge", callback_data="Take revenge")

    markup = [[Buttons.End_game], [Buttons.Take_revenge]]
    return InlineKeyboardBuilder(markup=markup).as_markup()


async def Axis():
    class Buttons:
        Axis_X = InlineKeyboardButton(text="Change to X", callback_data="Axis X")
        Axis_Y = InlineKeyboardButton(text="Change to Y", callback_data="Axis Y")
        Axis_Z = InlineKeyboardButton(text="Change to Z", callback_data="Axis Z")

    markup = [[Buttons.Axis_X], [Buttons.Axis_Y], [Buttons.Axis_Z]]
    return InlineKeyboardBuilder(markup=markup).as_markup()

