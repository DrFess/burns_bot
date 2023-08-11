from aiogram.types import Message

from db.commands import one_user


def are_you_moder(message: Message):
    if one_user(message.from_user.id):
        return True
    else:
        return False
