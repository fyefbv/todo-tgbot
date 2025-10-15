from asyncio import sleep
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.keyboards import tasks
from app.db.operations import set_task, del_task


task_router = Router()

last_message_ids = {}

TASKS_MESSAGE = (
    "Для добавления задачи напишите её в чат.\n"
    "Для удаления задачи нажмите на неё.\n"
    "Ваши задачи:"
)

@task_router.message(Command("tasks"))
async def tasks_message(message: Message):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    user_id = message.from_user.id
    keyboard = await tasks(user_id)

    if user_id in last_message_ids:  
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=last_message_ids[user_id]
            )
        except Exception as e:
            print(f"Не удалось удалить предыдущее сообщение: {e}")

    sent_message = await message.answer(TASKS_MESSAGE, reply_markup=keyboard)
    last_message_ids[user_id] = sent_message.message_id

@task_router.message(F.text)
async def add_task(message: Message):
    if len(message.text) > 100:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        notification = await message.answer("Задача должна содержать не более 100 символов")

        await sleep(3)
        await notification.delete()
    else:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        user_id = message.from_user.id
        await set_task(user_id, message.text)
        keyboard = await tasks(user_id)

        try:
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_message_ids[user_id],
                text=TASKS_MESSAGE, 
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Не удалось отредактировать предыдущее сообщение: {e}")

            sent_message = await message.answer(TASKS_MESSAGE, reply_markup=keyboard)
            last_message_ids[user_id] = sent_message.message_id

@task_router.callback_query(F.data.startswith("task_"))
async def delete_task(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    await del_task(task_id)
    
    keyboard = await tasks(callback.from_user.id)
    await callback.message.edit_text(TASKS_MESSAGE, reply_markup=keyboard)