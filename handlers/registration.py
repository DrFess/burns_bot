from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message

from buttons.keyboards import main_menu
from db.commands import add_user

router = Router()


@router.message(Text(text='Регистрация'))
async def user_registration(message: Message):
    if add_user(telegram_id=message.from_user.id, username=message.from_user.username or None):
        await message.answer('Теперь мы знакомы!', reply_markup=main_menu)
    else:
        await message.answer('Что-то пошло не так')
