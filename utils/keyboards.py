from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.LEXICON_RU import LEXICON
from handlers.keyboards.keyboards import __back_button

def trainer_list_markup(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    leftButton = InlineKeyboardButton(text='<', callback_data='previous_page')
    rightButton = InlineKeyboardButton(text='>', callback_data='next_page')
    page = InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='pages')
    choose = InlineKeyboardButton(text=f'Выбрать', callback_data='choose_this_trainer')

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [leftButton,
            page,
            rightButton],
            [choose],
            [__back_button[0][0]]
        ]
    )

def clients_list_markup(current_page: int, total_pages: int) -> InlineKeyboardButton:
    leftButton = InlineKeyboardButton(text='<', callback_data='previous_page')
    rightButton = InlineKeyboardButton(text='>', callback_data='next_page')
    page = InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='pages')
    create_plan = InlineKeyboardButton(text=f'Создать тренировочный план✍️', callback_data='create_training_plan')
    add_progress_report = InlineKeyboardButton(text=f'Написать отчет о прогрессе📝', callback_data='add_progress_report')

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [leftButton,
            page,
            rightButton],
            [create_plan],
            [add_progress_report],
            [__back_button[0][0]]
        ]
    )

def training_plan_markup(current_page: int, total_pages: int) -> InlineKeyboardButton:
    leftButton = InlineKeyboardButton(text='<', callback_data='previous_page')
    rightButton = InlineKeyboardButton(text='>', callback_data='next_page')
    page = InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='pages')


    return InlineKeyboardMarkup(
        inline_keyboard=[
            [leftButton,
            page,
            rightButton],
            [__back_button[0][0]]
        ]
    )

def progress_report_markup(current_page: int, total_pages: int) -> InlineKeyboardButton:
    leftButton = InlineKeyboardButton(text='<', callback_data='previous_page')
    rightButton = InlineKeyboardButton(text='>', callback_data='next_page')
    page = InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='pages')

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [leftButton,
            page,
            rightButton],
            [__back_button[0][0]]
        ]
    )

def metrics_report_markup(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    leftButton = InlineKeyboardButton(text='<', callback_data='previous_page')
    rightButton = InlineKeyboardButton(text='>', callback_data='next_page')
    page = InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='pages')

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [leftButton,
            page,
            rightButton],
            [__back_button[0][0]]
        ]
    )