from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from buttons.keyboards import index_menu
from db.commands import get_all_cases

router = Router()


@router.message(Text(text='Получить результаты'))
async def menu_cases(message: Message):
    data = get_all_cases()
    builder = InlineKeyboardBuilder()
    for case in data:
        builder.add(InlineKeyboardButton(text=f'{case.case_id}', callback_data=case.case_id))
    await message.answer('Выбери случай:', reply_markup=builder.as_markup())


@router.callback_query() #через FSM???
async def menu_results(callback: CallbackQuery):
    data = callback.data
    await callback.message.answer('Выбери показатель', reply_markup=index_menu)
