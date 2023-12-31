from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from buttons.keyboards import index_menu, back_button
from db.commands import get_all_cases, get_eaten_per_time, get_drunk_per_time, get_urine_per_time, get_calla_per_time
from utils.calculations import calculate_hydrobalance, calculate_date, indicators_per_time

router = Router()


class Results(StatesGroup):
    start = State()
    case = State()
    date = State()


@router.message(Text(text='Получить результаты'))
async def menu_cases(message: Message, state: FSMContext):
    await state.set_state(Results.start)
    data = get_all_cases()
    builder = InlineKeyboardBuilder()
    for case in data:
        builder.add(InlineKeyboardButton(text=f'{case.case_id}', callback_data=case.case_id))
    await message.answer('Выбери случай:', reply_markup=builder.as_markup())


@router.callback_query(Results.start)
async def menu_results(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    await state.update_data(
        case=data
    )
    await state.set_state(Results.case)
    await callback.message.answer('Выбери показатель', reply_markup=index_menu)


@router.callback_query(Text(text=['total']), Results.case)
async def per_hours(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Укажите за какой промежуток времени нужно рассчитать (в часах)')
    await state.set_state(Results.date)


@router.message(Results.date)
async def show_summary_data(message: Message, state: FSMContext):
    case = await state.get_data()
    date = calculate_date(message.text)
    eaten = indicators_per_time(int(case['case']), date, get_eaten_per_time)
    drunk = indicators_per_time(int(case['case']), date, get_drunk_per_time)
    urine = indicators_per_time(int(case['case']), date, get_urine_per_time)
    calla = indicators_per_time(int(case['case']), date, get_calla_per_time)
    diuresis_temp = calculate_hydrobalance(int(case['case']), date, int(message.text))
    await message.answer(f'За указанное время ({message.text}ч.)\n'
                         f'Выпито: {drunk:.>20} мл\n'
                         f'Получено мочи: {urine:.>20} мл\n'
                         f'Темп диуреза: {diuresis_temp:.>20} мл/кг/час\n'
                         f'Съедено: {eaten:.>20}\n'
                         f'Стул был раз: {calla:.>20}\n',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[back_button], resize_keyboard=True)
                         )
    await state.clear()
