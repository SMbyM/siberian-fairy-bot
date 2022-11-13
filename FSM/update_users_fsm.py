from aiogram.fsm.state import StatesGroup, State


class UpdateUser(StatesGroup):
    input_id = State()
    update_name = State()
    update_lastname = State()
    update_team = State()
    update_amount = State()
