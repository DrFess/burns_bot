import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

from buttons.keyboards import registration_kb, case_registration
from db.commands import check_user
from handlers import registration, adding_case, record_observations, get_results

bot = Bot(token='5915501320:AAH_XlpU5PGh0SB2FNu5uOhKgft32VAtHeo', parse_mode="HTML")
router = Router()


@router.message(Command(commands=["start", "menu"]))
async def command_start_handler(message: Message):
    if check_user(message.from_user.id):
        await message.answer(
            f"Привет {message.from_user.username}, это помощник врачей отделения термической травмы",
            reply_markup=case_registration
        )
    else:
        await message.answer(f'Привет! Мы ещё не знакомы. Давай зарегистрируемся?', reply_markup=registration_kb)


async def main():
    dp = Dispatcher()
    dp.include_routers(
        router,
        registration.router,
        adding_case.router,
        record_observations.router,
        get_results.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
