from aiogram.fsm.state import StatesGroup, State


# Состояния выбора роли и регистрации
class Start(StatesGroup):
    # Клиентский опрос
    get_height_state = State()
    get_weight_state = State()
    get_fat_state = State()

    # Тренерский опрос
    get_qualification_state = State()
    get_experience_state = State()
    get_achievements_state = State()

    get_photo_state = State()
    
    