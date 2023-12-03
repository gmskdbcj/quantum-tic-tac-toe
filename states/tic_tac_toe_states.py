from aiogram.filters.state import State, StatesGroup

class GameStates(StatesGroup):
    start = State()
    choosing_turn = State()
    choosing_gate = State()
    choosing_axis = State()
    wait = State()
    end = State()
