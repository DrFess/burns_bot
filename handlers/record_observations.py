from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from buttons.keyboards import metering_menu, main_menu
from db.commands import get_all_cases, add_one_drink, add_one_eaten, add_one_calla, add_one_urine

router = Router()


class Observation(StatesGroup):
    choose = State()
    allocation = State()
    eaten = State()
    drink = State()
    calla = State()
    urine = State()


@router.message(Text(text='Случай уже есть. Перейти к вводу данных'))
async def show_all_cases(message: Message, state: FSMContext):
    data = get_all_cases()
    builder = InlineKeyboardBuilder()
    for case in data:
        builder.add(InlineKeyboardButton(text=f'{case.case_id}', callback_data=case.case_id))
    await message.answer('Выбери случай:', reply_markup=builder.as_markup())
    await state.set_state(Observation.choose)


@router.callback_query(Observation.choose)
async def choose_case(callback: CallbackQuery, state: FSMContext):
    await state.update_data(
        case_id=callback.data
    )
    await callback.message.answer(
        f'Выберите какой показатель добавить для случая {callback.data}',
        reply_markup=metering_menu
    )
    await state.set_state(Observation.allocation)


@router.message(Observation.allocation)
async def input_data(message: Message, state: FSMContext):
    if 'Сколько съедено' in message.text:
        await state.set_state(Observation.eaten)
        await message.answer('Примерно сколько грамм было съедено за последний прием пищи?')
    elif 'Сколько выпито' in message.text:
        await state.set_state(Observation.drink)
        await message.answer('Введите объем выпитой жидкости в мл')
    elif 'Стул(количество раз за день)' in message.text:
        await state.set_state(Observation.calla)
        await message.answer('Сколько раз был стул?')
    elif 'Разовая порция мочи' in message.text:
        await state.set_state(Observation.urine)
        await message.answer('Введите объем полученной порции мочи в мл')
    elif f'\U0001F519 Назад' in message.text:
        await state.clear()
        await message.answer(
            f"Привет {message.from_user.username}, это помощник врачей отделения термической травмы",
            reply_markup=main_menu
        )
    else:
        await state.clear()
        await message.answer('Не понимаю тебя((', reply_markup=main_menu)


@router.message(Observation.eaten)
async def input_eaten(message: Message, state: FSMContext):
    case_id = await state.get_data()
    data = message.text
    add_one_eaten(
        case_id=case_id['case_id'],
        data=data,
    )
    await message.answer('Запись о количестве съеденной еды добавлена. Продолжим вводить данные?', reply_markup=metering_menu)
    await state.set_state(Observation.allocation)


@router.message(Observation.drink)
async def input_drink(message: Message, state: FSMContext):
    case_id = await state.get_data()
    data = message.text
    add_one_drink(
        case_id=case_id['case_id'],
        data=data,
    )
    await message.answer('Запись о количестве выпитого добавлена. Продолжим вводить данные?', reply_markup=metering_menu)
    await state.set_state(Observation.allocation)


@router.message(Observation.calla)
async def input_calla(message: Message, state: FSMContext):
    case_id = await state.get_data()
    data = message.text
    add_one_calla(
        case_id=case_id['case_id'],
        data=data,
    )
    await message.answer('Запись о количестве раз стула добавлена. Продолжим вводить данные?', reply_markup=metering_menu)
    await state.set_state(Observation.allocation)


@router.message(Observation.urine)
async def input_calla(message: Message, state: FSMContext):
    case_id = await state.get_data()
    data = message.text
    add_one_urine(
        case_id=case_id['case_id'],
        data=data,
    )
    await message.answer('Запись о количестве полученной мочи добавлена. Продолжим вводить данные?', reply_markup=metering_menu)
    await state.set_state(Observation.allocation)
