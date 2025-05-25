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
from state.menu import Menu
from handlers.start import send_client_menu, send_trainers_menu, delete_messages
from utils.keyboards import *
from repo.models.user import User
from datetime import datetime

rt = Router()

@rt.callback_query(F.data == 'profile',  StateFilter(Menu.client_main_menu))
async def client_profile_press(cb: CallbackQuery, cp_client: ChadProgressClient, cp_db: ChadProgressDB, state: FSMContext):
    token = await get_token(state)
    photo_id = await cp_db.get_photo_id(cb.from_user.id)
    
    resp = cp_client.get_client_profile(token).json()
    height, weight, fat = resp.get('height'), resp.get('weight'), resp.get('bodyfat')
    
    await cb.message.answer_photo(caption=f"Ваш профиль✨\nТекущий рост: {height}см\nТекущий вес: {weight}кг\nТекущий процент жира: {fat}%", photo=photo_id, reply_markup=back_markup)
    await cb.message.delete()
    

@rt.callback_query(F.data == 'profile', StateFilter(Menu.trainer_main_menu))
async def trainer_profile_press(cb: CallbackQuery, cp_client: ChadProgressClient, cp_db: ChadProgressDB, state: FSMContext):
    token = await get_token(state)
    photo_id = await cp_db.get_photo_id(cb.from_user.id)

    resp = cp_client.get_trainer_profile(token).json()
    qualification = resp.get('qualification')
    experience = resp.get('experience')
    achievements = resp.get('achievements')
    
    await cb.message.answer_photo(caption=f"Ваш профиль✨\nКвалификация: {qualification}\nОпыт: {experience}\nДостижения: {achievements}", photo=photo_id, reply_markup=back_markup)
    await cb.message.delete()

@rt.callback_query(F.data == 'training_plan', StateFilter(Menu.client_main_menu))
async def training_plan_press(cb: CallbackQuery, cp_client: ChadProgressClient, state: FSMContext):
    token = await get_token(state)

    client = cp_client.get_client_profile(token).json()
    trainer = cp_client.get_trainer_profile(token, client['trainer-id']).json()
    trainer_user_profile = cp_client.get_user_by_id(token, trainer['user-id']).json()

    plan = cp_client.get_plan(token, client['trainer-id'], client['id']).json()[0]
    
    sent = await cb.message.answer(
        text=f'Составил тренировочный план: {trainer_user_profile['name']}💪\nОписание: {plan['description']}\nРасписание: {plan['schedule']}',
        reply_markup=training_plan_markup(1, 1)
    )

    await state.update_data(to_delete=[sent.message_id])
    await cb.message.delete()

@rt.callback_query(F.data == 'reports', StateFilter(Menu.client_main_menu))
async def progress_report_press(cb: CallbackQuery, cp_client: ChadProgressClient, state: FSMContext):
    token = await get_token(state)

    client = cp_client.get_client_profile(token).json()
    trainer = cp_client.get_trainer_profile(token, client['trainer-id']).json()
    trainer_user_profile = cp_client.get_user_by_id(token, trainer['user-id']).json()

    report = cp_client.get_progress_reports(token, client['trainer-id'], client['id']).json()[0]
    sent = await cb.message.answer(
        text=f'Составил Вам отчет: {trainer_user_profile['name']}💪\nОтчет: {report['Comments']}',
        reply_markup=progress_report_markup(1, 1)
    )

    await state.update_data(to_delete=[sent.message_id])
    await cb.message.delete()

@rt.callback_query(F.data == 'metrics', StateFilter(Menu.client_main_menu))
async def metrics_press(cb: CallbackQuery, cp_client: ChadProgressClient, state: FSMContext):
    await cb.message.answer(
        text=LEXICON['metrics'],
        reply_markup=metrics_markup
    )

    await cb.message.delete()

@rt.callback_query(F.data == 'add_metrics', StateFilter(Menu.client_main_menu))
async def add_metrics_press(cb: CallbackQuery, state: FSMContext):
    await state.set_state(Menu.get_metrics)

    sent = await cb.message.answer(
        text=LEXICON['send_metrics'],
        reply_markup=cancel_markup
    )
    await cb.message.delete()

    await state.update_data(to_delete=[sent.message_id])

@rt.callback_query(F.data == 'cancel', StateFilter(Menu.get_metrics))
async def cancel_get_metrics_press(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await delete_messages(cb.message, data['to_delete'])
    
    sent = await cb.message.answer(
        text=LEXICON['metrics'],
        reply_markup=metrics_markup
    )
    await state.update_data(to_delete=[sent.message_id])
    await state.set_state(Menu.client_main_menu)

@rt.message(StateFilter(Menu.get_metrics))
async def metrics_message(msg: Message, cp_client: ChadProgressClient, state: FSMContext):
    data = await state.get_data()

    await delete_messages(msg, data['to_delete'])
    metrics = msg.text.split()
    if len(metrics) != 3:
        sent = await msg.answer(
            text=f'Неверный формат!\n{LEXICON["send_metrics"]}'
        )
        await msg.delete()
        
        await state.update_data(to_delete=[sent.message_id])

        return
    
    try:
        token = await get_token(state)

        metrics_float = list(map(float, metrics))
        height, weight, bodyfat = metrics_float[0], metrics_float[1], metrics_float[2]
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cp_client.add_metrics(token, height, weight, bodyfat, bmi, now)
        
        await state.set_state(Menu.client_main_menu)
        
        await msg.answer(
            text=LEXICON['metrics'],
            reply_markup=metrics_markup
        )
    except Exception:
        sent = await msg.answer(
            text=f'Неверный формат!\n{LEXICON["send_metrics"]}'
        )

        await msg.delete()
        
        await state.update_data(to_delete=[sent.message_id])


@rt.callback_query(F.data == 'check_metrics', StateFilter(Menu.client_main_menu))
async def check_metrics_press(cb: CallbackQuery, cp_client: ChadProgressClient, state: FSMContext ):
    token = await get_token(state)
    
    metrics = cp_client.get_metrics(token).json()
    if len(metrics) == 0:
        await cb.answer(text='Вы еще не добавляли метрики!')

        return
    
    await state.update_data(metrics=metrics)
    await state.update_data(current_page=1)
    
    metric = metrics[0]

    measured_at = metric['measured-at']
    height = metric['height']
    weight = metric['weight']
    body_fat = metric['bodyfat']
    bmi = metric['bmi']

    sent = await cb.message.answer(
        text=await make_metric_text(
            measured_at,
            height,
            weight,
            body_fat,
            bmi
        ),
        reply_markup=metrics_report_markup(1, len(metrics))
    )
    await cb.message.delete()

    await state.update_data(to_delete=[sent.message_id])
    await state.set_state(Menu.metrics_view)

@rt.callback_query(F.data == 'next_page', StateFilter(Menu.metrics_view))
async def next_page_metrics(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    metrics = data['metrics']

    current_page = data['current_page']
    if current_page == len(metrics):
        await cb.answer()
        
        return

    metric = metrics[current_page]

    measured_at = metric['measured-at']
    height = metric['height']
    weight = metric['weight']
    body_fat = metric['bodyfat']
    bmi = metric['bmi']

    await cb.message.edit_text(
        text=await make_metric_text(
            measured_at,
            height,
            weight,
            body_fat,
            bmi
        ),
        reply_markup=metrics_report_markup(current_page+1, len(metrics))
    )
    await state.update_data(current_page=current_page+1)


@rt.callback_query(F.data == 'previous_page', StateFilter(Menu.metrics_view))
async def prev_page_metrics(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    metrics = data['metrics']

    current_page = data['current_page']
    if current_page == 1:
        await cb.answer()

        return

    metric = metrics[current_page-2]

    measured_at = metric['measured-at']
    height = metric['height']
    weight = metric['weight']
    body_fat = metric['bodyfat']
    bmi = metric['bmi']

    await cb.message.edit_text(
        text=await make_metric_text(
            measured_at,
            height,
            weight,
            body_fat,
            bmi
        ),
        reply_markup=metrics_report_markup(current_page-1, len(metrics))
    )
    await state.update_data(current_page=current_page-1)

@rt.callback_query(F.data == 'choose_trainer', StateFilter(Menu.client_main_menu))
async def choose_trainer_press(cb: CallbackQuery, cp_client: ChadProgressClient, cp_db: ChadProgressDB, state: FSMContext):
    token = await get_token(state)

    resp = cp_client.get_trainers_list(token).json()
    if len(resp) == 0:
        await cb.answer(text='На данный момент нет активных тренеров')

        return
    
    dummy_trainer = resp[0]
    qualification = dummy_trainer['qualification']
    experience = dummy_trainer['experience']
    achievements = dummy_trainer['achievements']
    trainer = await cp_db.get_user(int(dummy_trainer['user-email']))

    about_trainer = f"{trainer.name}\nКвалификация: {qualification}\nОпыт: {experience}\nДостижения: {achievements}"
    photo_id = trainer.photo_id
    
    await cb.message.answer_photo(
        photo=photo_id,
        caption=about_trainer,
        reply_markup=trainer_list_markup(current_page=1, total_pages=len(resp)))
    await cb.message.delete()


@rt.callback_query(F.data == 'choose_this_trainer', StateFilter(Menu.client_main_menu))
async def choose_this_trainer_press(cb: CallbackQuery, cp_client: ChadProgressClient, state: FSMContext):
    token = await get_token(state)
    trainer_id = 2

    resp = cp_client.select_trainer(token, trainer_id)
    if not resp.ok:
        await cb.answer(text=LEXICON['server_error'])
        return
    
    await cb.answer("Тренер выбран")
    await send_client_menu(cb.message)
    await cb.message.delete()

@rt.callback_query(F.data == 'clients_list', StateFilter(Menu.trainer_main_menu))
async def clients_list_press(cb: CallbackQuery, cp_client: ChadProgressClient, cp_db: ChadProgressDB, state: FSMContext):
    token = await get_token(state)
    
    clients_list = cp_client.get_trainers_clients(token)

    client = clients_list.json()[0]
    user = cp_client.get_user_by_id(token, int(client['user-id'])).json()
    tg_user: User = await cp_db.get_user(int(user['email']))
    caption = f'{user['name']}\nРост: {client['height']}см\nВес: {client['weight']}кг\nПроцент жира: {client['bodyfat']}%'
    await cb.message.answer_photo(
        caption=caption,
        photo=tg_user.photo_id,
        reply_markup=clients_list_markup(1, len(clients_list.json()))
    )
    await cb.message.delete()

@rt.callback_query(F.data == 'create_training_plan', StateFilter(Menu.trainer_main_menu))
async def create_training_plan(cb: CallbackQuery, cp_client: ChadProgressClient, cp_db: ChadProgressDB, state: FSMContext):
    sent = await cb.message.answer("Пришлите описание тренировочного плана🦾")
    await state.set_state(Menu.get_description)
    await state.update_data(to_delete=[sent.message_id])
   
    await cb.message.delete()

@rt.message(StateFilter(Menu.get_description))
async def get_description(msg: Message, state: FSMContext):
    data = await state.get_data()
    await delete_messages(msg, data['to_delete'])

    await state.update_data(description=msg.text)
    sent = await msg.answer('Пришлите распанисание тренировки текстом🗓')
    await state.update_data(to_delete=[sent.message_id])

    await state.set_state(Menu.get_schedule)

@rt.message(StateFilter(Menu.get_schedule))
async def get_schedule(msg: Message, cp_client: ChadProgressClient, cp_db: ChadProgressDB, state: FSMContext):
    token = await get_token(state)

    data = await state.get_data()
    await delete_messages(msg, data['to_delete'])

    description = data['description']
    schedule = msg.text

    cp_client.create_plan(token, 1, description, schedule)
    
    await msg.answer("План создан успешно✅")
    await send_trainers_menu(msg)
    await state.set_state(Menu.trainer_main_menu)

@rt.callback_query(F.data == 'add_progress_report', StateFilter(Menu.trainer_main_menu))
async def create_progress_report(cb: CallbackQuery, cp_client: ChadProgressClient, cp_db: ChadProgressDB, state: FSMContext):
    sent = await cb.message.answer("Пришлите комментарии клиенту, по поводу его прогресса💬")
    await state.update_data(to_delete=[sent.message_id])

    await cb.message.delete()

    await state.set_state(Menu.get_comments)
    

@rt.message(StateFilter(Menu.get_comments))
async def get_comment_message(msg: Message, cp_client: ChadProgressClient, cp_db: ChadProgressDB, state: FSMContext):
    data = await state.get_data()
    await delete_messages(msg, data['to_delete'])
    
    token = await get_token(state)
    comment = msg.text
    
    cp_client.add_progress_report(token, 1, comment)

    await msg.answer("Комментарий успешно оставлен клиенту✅")
    await send_trainers_menu(msg)
    await state.set_state(Menu.trainer_main_menu)

@rt.callback_query(F.data == 'back', StateFilter(Menu.client_main_menu))
async def back_from_client_profile(cb: CallbackQuery):
    await send_client_menu(cb.message)
    await cb.message.delete()

@rt.callback_query(F.data == 'back', StateFilter(Menu.trainer_main_menu))
async def back_from_trainer_profile(cb: CallbackQuery):
    await send_trainers_menu(cb.message)
    await cb.message.delete()

@rt.callback_query(F.data == 'back', StateFilter(Menu.metrics_view))
async def back_from_metrics_view(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer(
        text=LEXICON['metrics'],
        reply_markup=metrics_markup
    )
    await cb.message.delete()
    await state.set_state(Menu.client_main_menu)


async def get_token(state: FSMContext):
    data = await state.get_data()
    
    return data['token']

async def make_metric_text(measured_at: str, height: str, weight: str, bodyfat: str, bmi: str) -> str:
    date_format = "%Y-%m-%d %H:%M:%S %z %Z"
    dt = datetime.strptime(measured_at, date_format)
    bmi_status = ""
    bmi_float = float(bmi)

    if bmi_float < 18.5:
        bmi_status = f'Недостаток массы тела🔴'
    elif 18.5 <= bmi_float < 25:
        bmi_status = f'Нормальный вес🟢'
    else:
        bmi_status = f'Ожирение🐷'

    return f"""Время измерения: {dt.strftime("%d.%m.%Y %H:%M")}
Рост: {height}см 📏
Вес: {weight}кг ⏲️
Процент жира: {bodyfat}% 🐷 ({weight*(bodyfat/100)} кг жира в теле)
Индекс массы тела: {bmi} ({bmi_status})"""