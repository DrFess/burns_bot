from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

registration_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Регистрация')]],
    one_time_keyboard=True,
    resize_keyboard=True
)

case_registration = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Зарегистрировать случай госпитализации')],
        [KeyboardButton(text='Случай уже есть. Перейти к вводу данных')],
        [KeyboardButton(text='Получить результаты')]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

true_or_false = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Верно!')],
        [KeyboardButton(text='Нет, нужно скорректировать информацию')]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

metering_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=u'\U0001F357 Сколько съедено')],
        [KeyboardButton(text=u'\u2615 Сколько выпито')],
        [KeyboardButton(text=u'\U0001F4A9 Стул(количество раз за день)')],
        [KeyboardButton(text='Разовая порция мочи')],
        [KeyboardButton(text=u'\U0001F519 Вернуться к прошлому меню')]
    ],
    resize_keyboard=True
)

index_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Сводные данные за время')],
        [KeyboardButton(text='показатель 3')],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

moderator_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Просмотреть всех пользователей без модерации')],
    ],
    resize_keyboard=True
)
