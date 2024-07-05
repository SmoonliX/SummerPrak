from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,ReplyKeyboardRemove

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Вакансии"), KeyboardButton(text="Резюме")]], resize_keyboard=True)


# Создание клавиатуры и добавление кнопок в виде списка списков
work_format_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Полный день')],
        [KeyboardButton(text='Удаленная работа')],
        [KeyboardButton(text='Гибкий график')],
        [KeyboardButton(text='Сменный график')],
        [KeyboardButton(text='Вахтовый метод')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Создание клавиатуры для опыта работы
experience_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Более 6 лет')],
        [KeyboardButton(text='От 3 до 6 лет')],
        [KeyboardButton(text='Нет опыта')],
        [KeyboardButton(text='От 1 года до 3 лет')]
    ],
    resize_keyboard=True,
one_time_keyboard=True
)

education_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Не требуется или не указано')],
        [KeyboardButton(text='Высшее')],
        [KeyboardButton(text='Среднее профессиональное')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)