from aiogram.filters.callback_data import CallbackData


class TurnCallbackFactory(CallbackData, prefix="turn"):
    action: str

class GateCallbackFactory(CallbackData, prefix="gate"):
    action: str

class StartCallbackFactory(CallbackData, prefix="start"):
    action: str

class EndCallbackFactory(CallbackData, prefix="end"):
    action: str

class WaitCallbackFactory(CallbackData, prefix="wait"):
    action: str

class AxisCallbackFactory(CallbackData, prefix="axis"):
    action: str
