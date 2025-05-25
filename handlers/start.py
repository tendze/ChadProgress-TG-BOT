from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from clients.chadprogress import ChadProgressClient
from handlers.keyboards.keyboards import *
from lexicon.LEXICON_RU import LEXICON
from repo.sqlite.sqlite import ChadProgressDB
from repo.models.enum import UserRole
from state.start import Start
from state.menu import Menu
from utils.password import generate_password

rt = Router()

@rt.message(CommandStart(), StateFilter(default_state))
async def start_handler(msg: Message, cp_client: ChadProgressClient, cp_db: ChadProgressDB, state: FSMContext):
    user = await cp_db.get_user(msg.from_user.id)
    if user:
        if user.role == UserRole.CLIENT.value:
            await state.set_state(Menu.client_main_menu)
            await send_client_menu(msg)
        else:
            await state.set_state(Menu.trainer_main_menu)
            await send_trainers_menu(msg)
        
        token = await cp_db.get_token(msg.from_user.id)
        await state.update_data(token=token)

        return
    
    await send_greetings(msg)

@rt.callback_query(F.data == 'role_client', StateFilter(default_state))
async def choose_client_press(cb: CallbackQuery, state: FSMContext):
    sent = await cb.message.answer(text=LEXICON['write_height'], reply_markup=cancel_markup)
    await state.update_data(to_delete=[sent.message_id])

    await cb.message.delete()
    await state.update_data(role='client')
    await state.set_state(Start.get_height_state)

@rt.callback_query(F.data == 'role_trainer', StateFilter(default_state))
async def choose_trainer_press(cb: CallbackQuery, state: FSMContext):
    sent = await cb.message.answer(text=LEXICON['write_qualification'], reply_markup=cancel_markup)
    await state.update_data(to_delete=[sent.message_id])

    await cb.message.delete()
    await state.update_data(role='trainer')
    await state.set_state(Start.get_qualification_state)

@rt.message(StateFilter(Start.get_height_state))
async def height_message_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    await delete_messages(msg, data.get('to_delete'))

    try:
        height_str = msg.text.strip().replace(",", ".")
        height = float(height_str)

        await state.update_data(height=height)
        await state.set_state(Start.get_weight_state)

        sent = await msg.answer(text=LEXICON['write_weight'], reply_markup=cancel_markup)
        await state.update_data(to_delete=[sent.message_id])
    except Exception as e:
        sent1, sent2 = await msg.answer(text='Некорректный формат роста!'), await msg.answer(text=LEXICON['write_height'], reply_markup=cancel_markup)
        await state.update_data(to_delete=[sent1.message_id, sent2.message_id])

    await msg.delete()

@rt.message(StateFilter(Start.get_weight_state))
async def weight_message_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    await delete_messages(msg, data.get('to_delete'))

    try:
        weight_str = msg.text.strip().replace(",", ".")
        weight = float(weight_str)

        await state.update_data(weight=weight)
        await state.set_state(Start.get_fat_state)

        sent = await msg.answer(text=LEXICON['write_fat_percent'], reply_markup=cancel_markup)
        await state.update_data(to_delete=[sent.message_id])
    except Exception as e:
        sent1, sent2 = await msg.answer(text='Некорректный формат веса!'), await msg.answer(text=LEXICON['write_weight'], reply_markup=cancel_markup)
        await state.update_data(to_delete=[sent1.message_id, sent2.message_id])

    await msg.delete()

@rt.message(StateFilter(Start.get_fat_state))
async def fat_message_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    await delete_messages(msg, data.get('to_delete'))

    try:
        fat_str = msg.text.strip().replace(",", ".")
        fat = float(fat_str)

        await state.update_data(fat=fat)
        await state.set_state(Start.get_photo_state)

        sent = await msg.answer(text=LEXICON['send_photo'], reply_markup=cancel_markup)
        await state.update_data(to_delete=[sent.message_id])
    except Exception as e:
        sent1, sent2 = await msg.answer(text='Некорректный формат!'), await msg.answer(text=LEXICON['write_fat_percent'], reply_markup=cancel_markup)
        await state.update_data(to_delete=[sent1.message_id, sent2.message_id])

    await msg.delete()

@rt.message(StateFilter(Start.get_qualification_state))
async def qualification_message_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    await delete_messages(msg, data.get('to_delete'))

    qualification = msg.text
    await state.update_data(qualification=qualification)
    await state.set_state(Start.get_experience_state)

    sent = await msg.answer(text=LEXICON['write_experience'], reply_markup=cancel_markup)
    await state.update_data(to_delete=[sent.message_id])

    await msg.delete()

@rt.message(StateFilter(Start.get_experience_state))
async def experience_message_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    await delete_messages(msg, data.get('to_delete'))

    experience = msg.text
    await state.update_data(experience=experience)
    await state.set_state(Start.get_achievements_state)

    sent = await msg.answer(text=LEXICON['write_achievements'], reply_markup=cancel_markup)
    await state.update_data(to_delete=[sent.message_id])
    await msg.delete()

@rt.message(StateFilter(Start.get_achievements_state))
async def achievements_message_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    await delete_messages(msg, data.get('to_delete'))

    achievements = msg.text
    await state.update_data(achievements=achievements)
    await state.set_state(Start.get_photo_state)

    sent = await msg.answer(text=LEXICON['send_photo'], reply_markup=cancel_markup)
    await state.update_data(to_delete=[sent.message_id])
    await msg.delete()

@rt.message(StateFilter(Start.get_photo_state), F.photo)
async def photo_message_answer(msg: Message, cp_client: ChadProgressClient, cp_db: ChadProgressDB, state: FSMContext):
    data = await state.get_data()
    await delete_messages(msg, data.get('to_delete'))

    data = await state.get_data()

    photo_id = msg.photo[-1].file_id
    login = str(msg.from_user.id)
    password = generate_password()
    name = msg.from_user.full_name
    role = data['role']
    token = cp_client.register(
        login,
        password,
        name,
        role
    )
    await cp_db.save_user(login, password, name, token, photo_id, role)
    if role == UserRole.CLIENT.value:
        height, weight, fat_percent = data['height'], data['weight'], data['fat']
        response = cp_client.create_client_profile(token, height, weight, fat_percent)
        if not response.ok:
            await msg.answer(text=LEXICON['server_error'])
            
        await state.set_state(Menu.client_main_menu)
        await send_client_menu(msg)
    else:
        qualification, experience, achievements = data['qualification'], data['experience'], data['achievements']
        response = cp_client.create_trainer_profile(token, qualification, experience, achievements)
        if not response.ok:
            await msg.answer(text=LEXICON['server_error'])

        await state.set_state(Menu.trainer_main_menu)
        await send_trainers_menu(msg)
    
    await state.update_data(token=token)
    await msg.delete()
    
@rt.callback_query(F.data == 'cancel', StateFilter(Start))
async def cancel_poll(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await delete_messages(cb.message, data.get('to_delete'))

    await send_greetings(cb.message)
    await state.clear()
    await cb.message.delete()

async def send_client_menu(msg: Message):
    await msg.answer(text=LEXICON['clients_menu'], reply_markup=clients_main_menu_markup)

async def send_trainers_menu(msg: Message):
    await msg.answer(text=LEXICON['trainers_menu'], reply_markup=trainers_main_menu_markup)

async def send_greetings(msg: Message):
    await msg.answer(text=LEXICON['start_greeting'], reply_markup=role_choice_markup)

async def delete_messages(msg: Message, message_ids: list[int]):
    if message_ids == None:
        return
    try: 
        for id in message_ids:
            await msg.bot.delete_message(chat_id=msg.chat.id, message_id=id)
    except Exception:
        pass