import datetime

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram3_calendar import SimpleCalendar

from buttons.keyboards import true_or_false, main_menu
from db.commands import add_case

router = Router()


class Case(StatesGroup):
    case_id = State()
    age = State()
    height = State()
    weight = State()
    date_start = State()
    confirmation = State()


@router.message(Text(text='Зарегистрировать случай госпитализации'))
async def add_user_id(message: Message, state: FSMContext):
    await state.set_state(Case.case_id)
    await state.update_data(
        user_id=message.from_user.id  # или запросить из базы данных User.telegram_id???
    )
    await message.answer('Пришли номер случая')


@router.message(Case.case_id)
async def add_case_id(message: Message, state: FSMContext):
    await state.update_data(
        case_id=int(message.text)
    )
    await state.set_state(Case.age)
    await message.answer('Теперь пришли возраст')


@router.message(Case.age)
async def add_age(message: Message, state: FSMContext):
    await state.update_data(
        age=int(message.text)
    )
    await state.set_state(Case.height)
    await message.answer('А теперь пришли рост в сантиметрах')


@router.message(Case.height)
async def add_height(message: Message, state: FSMContext):
    await state.update_data(
        height=int(message.text)
    )
    await state.set_state(Case.weight)
    await message.answer('Ещё нужен вес в килограммах')


@router.message(Case.weight)
async def add_date_start(message: Message, state: FSMContext):
    await state.update_data(
        weight=int(message.text)
    )
    await state.set_state(Case.date_start)
    await message.answer('И осталось выбрать дату начала случая', reply_markup=await SimpleCalendar().start_calendar())


@router.callback_query(Case.date_start)
async def end_case(callback_query: CallbackQuery, state: FSMContext):
    date = callback_query.data.split(':')
    year = date[2]
    month = date[3]
    day = date[4]
    await state.update_data(
        year=int(year),
        month=int(month),
        day=int(day)
    )
    await state.set_state(Case.confirmation)
    data = await state.get_data()
    await callback_query.message.answer(
        f'Что у нас получилось:\n'
        f'Номер случая {data["case_id"]}\n'
        f'Возраст {data["age"]}\n'
        f'Рост {data["height"]}\n'
        f'Вес {data["weight"]}\n'
        f'Дата начала случая {day}.{month}.{year}\n'
        f'Всё верно?',
        reply_markup=true_or_false
    )


@router.message(Case.confirmation, Text(text='Верно!'))
async def database_entry(message: Message, state: FSMContext):
    data = await state.get_data()
    add_case(
        case_id=data['case_id'],
        user_id=data['user_id'],
        date_start=datetime.date(data['year'], data['month'], data['day']),
        age=data['age'],
        height=data['height'],
        weight=data['weight'],
    )
    await message.answer('Случай добавлен')
    await state.clear()


@router.message(Case.confirmation, Text(text='Нет, нужно скорректировать информацию'))
async def again_case(message: Message, state: FSMContext):
    await message.answer('Начинаем регистрацию заново', reply_markup=main_menu)
    await state.clear()
