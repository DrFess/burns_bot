import datetime

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from buttons.keyboards import index_menu
from db.commands import get_all_cases
from utils.calculations import calculate_hydrobalance

router = Router()


class Results(StatesGroup):
    start = State()
    case = State()
    date = State()
    hydrobalance = State()


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


@router.message(Text(text='Гидробаланс'), Results.case)
async def per_hours(message: Message, state: FSMContext):
    await message.answer('Укажите за какой промежуток времени нужно рассчитать (в часах)')
    await state.set_state(Results.date)


@router.message(Results.date)
async def get_hydrobalance(message: Message, state: FSMContext):
    delta = datetime.timedelta(hours=float(message.text))
    search_date = datetime.datetime.now() - delta
    case = await state.get_data()
    result = calculate_hydrobalance(int(case['case']), search_date, int(message.text))
    await message.answer(f'Диурез за указанное время({message.text}ч.) составил {result} мл/кг/час.')
