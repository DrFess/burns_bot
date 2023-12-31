import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from buttons.keyboards import registration_kb, main_menu, moderator_menu
from db.commands import check_user
from db.models import create_table
from handlers import registration, adding_case, record_observations, get_results, moderations

bot = Bot(token=os.getenv('TOKEN'), parse_mode="HTML")
router = Router()


@router.message(Command(commands=["start", "menu"]))
async def command_start_handler(message: Message):
    if check_user(message.from_user.id):
        await message.answer(
            f"Привет {message.from_user.username}, это помощник врачей отделения термической травмы\n"
            f"Подсказки лежат по команде /info",
            reply_markup=main_menu
        )
    else:
        await message.answer(f'Привет! Мы ещё не знакомы. Давай зарегистрируемся?', reply_markup=registration_kb)


@router.message(Command(commands=['info']))
async def info(message: Message):
    await message.answer('Команды /start и /menu перезапустят бота\n'
                         'Команда /moderate включит режим модератора\n'
                         'Команда /delete_moderator удалить пользователя из модераторов\n'
                         'Команда /delete_cases удалит все не активные случаи')


@router.message(Command(commands=['moderate']))
async def moderate_menu(message: Message):
    await message.answer('Включен режим модератора.', reply_markup=moderator_menu)


@router.message(Text(text='\U0001F519 Назад'))
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Основное меню', reply_markup=main_menu)


async def main():
    dp = Dispatcher()
    dp.include_routers(
        router,
        registration.router,
        adding_case.router,
        record_observations.router,
        get_results.router,
        moderations.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    create_table()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
