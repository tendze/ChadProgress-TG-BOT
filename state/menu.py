from aiogram.fsm.state import StatesGroup, State


# Состояния выбора роли и регистрации
class Menu(StatesGroup):
    client_main_menu = State()

    trainer_main_menu = State()

    get_description = State()
    get_schedule = State()

    get_comments = State()

    get_metrics = State()

    metrics_view = State()
    