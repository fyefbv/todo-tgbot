from asyncio import sleep
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.db.operations import set_user
from app.handlers.task import tasks_message


user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await tasks_message(message)

@user_router.message(F.photo | F.video | F.animation | F.contact | F.document | F.sticker)
async def handle_media(message: Message):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
    notification = await message.answer("Отправлять можно только текст")

    await sleep(3)
    await notification.delete()