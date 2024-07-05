from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import database.requests as rq
from app import keyboards as kb
from app.parsers.parser_vacancies import extract_vacancies

# Изначальный URL
BASE_URL = 'https://hh.ru/search/vacancy'
router = Router()


# Функция для обновления параметров URL
def update_url(params):
    url_parts = list(urlparse(BASE_URL))
    query = parse_qs(url_parts[4], keep_blank_values=True)  # keep_blank_values=True для сохранения пустых значений
    query.update(params)
    url_parts[4] = urlencode(query, doseq=True)
    return urlunparse(url_parts)


class Vacancy(StatesGroup):
    position = State()
    skills = State()
    work_format = State()
    experience = State()
    education = State()


@router.message(F.text.lower() == "вакансии")
async def start_vacancy(message: Message, state: FSMContext):
    await state.set_state(Vacancy.position)
    await message.answer("Введите позицию, должность")


@router.message(Vacancy.position)
async def cmd_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    await state.set_state(Vacancy.skills)
    await message.answer("Введите желаемые навыки кандидата")


@router.message(Vacancy.skills)
async def cmd_skills(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await state.set_state(Vacancy.work_format)
    await message.answer("Выберите формат работы", reply_markup=kb.work_format_kb)


@router.message(Vacancy.work_format)
async def cmd_work_format(message: Message, state: FSMContext):
    await state.update_data(work_format=message.text)
    await state.set_state(Vacancy.experience)
    await message.answer("Выберите желаемый опыт работы", reply_markup=kb.experience_kb)


@router.message(Vacancy.experience)
async def cmd_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(Vacancy.education)
    await message.answer("Выберите образование", reply_markup=kb.education_kb)


@router.message(Vacancy.education)
async def cmd_education(message: Message, state: FSMContext):
    await state.update_data(education=message.text)
    data = await state.get_data()

    # Определение параметров для обновления URL
    experience_mapping = {
        'Более 6 лет': 'moreThan6',
        'От 3 до 6 лет': 'between3And6',
        'Нет опыта': 'noExperience',
        'От 1 года до 3 лет': 'between1And3'
    }
    education_mapping = {
        'Не требуется или не указано': 'not_required_or_not_specified',
        'Высшее': 'higher',
        'Среднее профессиональное': 'special_secondary'
    }
    experience_param = experience_mapping.get(data['experience'], '')
    education_param = education_mapping.get(data['education'], '')

    search_text = f"{data['position']} {data['skills']}"
    params = {
        'text': search_text,
        'salary': '',
        'ored_clusters': 'true',
        'experience': experience_param,
        'education': education_param,
        'area': '113',
        'hhtmFrom': 'vacancy_search_list',
        'hhtmFromLabel': 'vacancy_search_line'
    }
    # Изначальный URL
    updated_url = update_url(params)
    await state.clear()
    await message.answer(f"Начинаем поиск... Вот ваш URL: {updated_url}")
    vacancies = extract_vacancies(updated_url)
    if len(vacancies) == 0:
        await message.answer("Вакансии не найдены")
        return

    vacancies_text = ""
    num = 1
    for vac in vacancies:
        vacancies_text += f"{num}. {vac['title']}\n Опыт: {vac['experience']}\nКомпания: {vac['company']}\nГород:{vac['city']}\n\n"
        num += 1
        if num == 11:
            break

    await message.answer(vacancies_text)
    for vac in vacancies:
        await rq.add_vacancy(
            title=vac['title'],
            experience=vac['experience'],
            company=vac['company'],
            city=vac['city'],
        )

@router.message(F.text)
async def cmd_text(message: Message):
    await message.answer('Выберите пункт меню!', reply_markup=kb.main)
