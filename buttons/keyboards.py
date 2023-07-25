from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import keyboard

registration_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Регистрация')]],
    one_time_keyboard=True,
    resize_keyboard=True
)

case_registration = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Зарегистрировать случай госпитализации')],
        [KeyboardButton(text='Случай уже есть. Перейти к вводу данных')]
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
        [KeyboardButton(text='Сколько съедено')],
        [KeyboardButton(text='Сколько выпито')],
        [KeyboardButton(text='Стул(количество раз за день)')],
        [KeyboardButton(text='Разовая порция мочи')],
    ],
    resize_keyboard=True
)