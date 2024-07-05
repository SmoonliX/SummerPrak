from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import database.requests as rq
from app import keyboards as kb
from app.parsers.parser_resume import extract_resumes

# Изначальный URL
BASE_URL = 'https://hh.ru/search/resume'
router = Router()


# Функция для обновления параметров URL
def update_url(params):
    url_parts = list(urlparse(BASE_URL))
    query = parse_qs(url_parts[4])
    query.update(params)
    url_parts[4] = urlencode(query, doseq=True)
    return urlunparse(url_parts)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в бот для поиска резюме!', reply_markup=kb.main)


class Resume(StatesGroup):
    position = State()
    skills = State()
    work_format = State()
    experience = State()


@router.message(F.text.lower() == "резюме")
async def start_resume(message: Message, state: FSMContext):
    await state.set_state(Resume.position)
    await message.answer("Введите позицию, должность")


@router.message(Resume.position)
async def cmd_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    await state.set_state(Resume.skills)
    await message.answer("Введите желаемые навыки кандидата")


@router.message(Resume.skills)
async def cmd_skills(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await state.set_state(Resume.work_format)
    await message.answer("Выберите формат работы", reply_markup=kb.work_format_kb)


@router.message(Resume.work_format)
async def cmd_work_format(message: Message, state: FSMContext):
    await state.update_data(work_format=message.text)
    await state.set_state(Resume.experience)
    await message.answer("Выберите желаемый опыт работы", reply_markup=kb.experience_kb)


@router.message(Resume.experience)
async def cmd_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    data = await state.get_data()

    # Определение параметров для обновления URL
    experience_mapping = {
        'Более 6 лет': 'moreThan6',
        'От 3 до 6 лет': 'between3And6',
        'Нет опыта': 'noExperience',
        'От 1 года до 3 лет': 'between1And3'
    }
    experience_param = experience_mapping.get(data['experience'], '')

    search_text = f"{data['position']} {data['skills']}"
    params = {
        'text': search_text,
        'area': '113',
        'isDefaultArea': 'true',
        'exp_period': 'all_time',
        'logic': 'normal',
        'pos': 'full_text',
        'page': '1',
        'customDomain': '1',
        'experience': experience_param
    }
    # Изначальный URL
    updated_url = update_url(params)
    await state.clear()
    await message.answer(f"Начинаем поиск... Вот ваш URL: {updated_url}")
    resumes = extract_resumes(updated_url)
    if len(resumes)==0:
        await message.answer("Резюме не найдены")
        return
    resumes_text = ""
    num = 1
    for res in resumes:
        resumes_text += f"{num}. {res['title']}\nВозраст: {res['age']}\nОпыт: {res['experience']} {res['link']}\n\n"
        num += 1
        if num == 11:
            break

    await  message.answer(resumes_text)
    for res in resumes:
        await rq.add_resume(
            title=res['title'],
            link=res['link'],
            age=res['age'],
            experience=res['experience'],
            last_job=res['last_job'],
            last_job_date=res['last_job_date'],
        )

