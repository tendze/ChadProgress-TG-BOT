from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.LEXICON_RU import LEXICON

__role_choice_buttons: list[list[InlineKeyboardButton]] = [
    [InlineKeyboardButton(text=LEXICON['role_client'], callback_data='role_client'),
      InlineKeyboardButton(text=LEXICON['role_trainer'], callback_data='role_trainer')]
]
role_choice_markup = InlineKeyboardMarkup(
    inline_keyboard=__role_choice_buttons
)

__clients_main_menu_buttons: list[list[InlineKeyboardButton]] = [
    [InlineKeyboardButton(text=LEXICON['choose_trainer'], callback_data='choose_trainer'),],
    [InlineKeyboardButton(text=LEXICON['metrics'], callback_data='metrics')],
    [InlineKeyboardButton(text=LEXICON['reports'], callback_data='reports')],
    [InlineKeyboardButton(text=LEXICON['training_plan'], callback_data='training_plan')],
    [InlineKeyboardButton(text=LEXICON['profile'], callback_data='profile')]
]
clients_main_menu_markup = InlineKeyboardMarkup(
    inline_keyboard=__clients_main_menu_buttons
)

__trainers_main_menu_buttons: list[list[InlineKeyboardButton]] = [
    [InlineKeyboardButton(text=LEXICON['choose_trainer'], callback_data='choose_trainer'),],
    [InlineKeyboardButton(text=LEXICON['create_plan'], callback_data='create_plan')],
    [InlineKeyboardButton(text=LEXICON['profile'], callback_data='profile')],
]
trainers_main_menu_markup = InlineKeyboardMarkup(
    inline_keyboard=__trainers_main_menu_buttons
)

__cancel_button: list[list[InlineKeyboardButton]] = [
    [InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel')]
]
cancel_markup = InlineKeyboardMarkup(
    inline_keyboard=__cancel_button
)