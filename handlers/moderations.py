from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from db.commands import show_users_without_moderation, give_moderation, show_moderators, delete_moderator, \
    get_all_cases, switch_case_status, delete_cases

router = Router()


class Moderation(StatesGroup):
    get_cases = State()
    change_case = State()


@router.message(Text(text='Просмотреть всех пользователей без модерации'))
async def give_all_users_without_moderation(message: Message):
    no_moders = show_users_without_moderation()
    if no_moders:
        builder = InlineKeyboardBuilder()
        for user in no_moders:
            builder.row(InlineKeyboardButton(text='Назначить модератором', callback_data=f'назначить {user[0]} {user[1]}'))
            await message.answer(f'{user[1]}', reply_markup=builder.as_markup())
    else:
        await message.answer('Нет пользователей без прав модератора')


@router.callback_query(Text(startswith='назначить'))
async def make_moderator(callback: CallbackQuery):
    user_id = int(callback.data.split(' ')[1])
    user = callback.data.split(' ')[2]
    give_moderation(user_id)
    await callback.message.answer(f'Пользователь {user} назначен модератором')


@router.message(Command(commands=['delete_moderator']))
async def delete_moderator_step1(message: Message):
    moders = show_moderators()
    if moders:
        builder = InlineKeyboardBuilder()
        for user in moders:
            builder.row(InlineKeyboardButton(text='убрать из модераторов', callback_data=f'удалить {user[0]} {user[1]}'))
            await message.answer(f'{user[1]} telegram ID: {user[0]}', reply_markup=builder.as_markup())
    else:
        await message.answer('Модераторов пока нет')


@router.callback_query(Text(startswith='удалить'))
async def delete_moderator_step2(callback: CallbackQuery):
    user_id = int(callback.data.split(' ')[1])
    user = callback.data.split(' ')[2]
    delete_moderator(user_id)
    await callback.message.answer(f'Пользователь {user} удален из модераторов')


@router.message(Text(text='Изменить статус случая'))
async def give_case_status(message: Message, state: FSMContext):
    await state.set_state(Moderation.get_cases)
    data = get_all_cases()
    for case in data:
        if case.is_active is True:
            await message.answer(f'{case.case_id} - Активный \u2705')
        else:
            await message.answer(f'{case.case_id} - Не активный \u274C')
    await message.answer('Пришлите номер случая чтобы изменить его статус')


@router.message(Moderation.get_cases)
async def change_case_status(message: Message, state: FSMContext):
    await state.set_state(Moderation.change_case)
    switch_case_status(int(message.text))
    data = get_all_cases()
    for case in data:
        if case.is_active is True:
            await message.answer(f'{case.case_id} - Активный \u2705')
        else:
            await message.answer(f'{case.case_id} - Не активный \u274C')
    await message.answer('Продолжим?')


@router.message(Moderation.change_case, Command(commands=['delete_cases']))
async def del_cases(message: Message, state: FSMContext):
    delete_cases()
    data = get_all_cases()
    for case in data:
        if case.is_active is True:
            await message.answer(f'{case.case_id} - Активный \u2705')
        else:
            await message.answer(f'{case.case_id} - Не активный \u274C')
    await state.clear()
