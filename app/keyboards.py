from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db.operations import get_tasks


async def tasks(tg_id):
    tasks = await get_tasks(tg_id)
    keyboard = InlineKeyboardBuilder()

    for task in tasks:
        keyboard.add(
            InlineKeyboardButton(text=task.task, callback_data=f'task_{task.id}')
        )

    return keyboard.adjust(1).as_markup()