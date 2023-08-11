from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

back_button = [KeyboardButton(text=f'\U0001F519 Назад')]

registration_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Регистрация')]],
    one_time_keyboard=True,
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Случай уже есть. Перейти к вводу данных')],
        [KeyboardButton(text='Получить результаты')],
        [KeyboardButton(text='Зарегистрировать случай госпитализации')],
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
        back_button
    ],
    resize_keyboard=True
)

index_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Сводные данные за время', callback_data='total')],
    ],
)

moderator_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Просмотреть всех пользователей без модерации')],
        [KeyboardButton(text='Изменить статус случая')],
        back_button
    ],
    resize_keyboard=True
)

change_status = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Изменить статус')],
        back_button
    ]
)
