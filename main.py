import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram import F

from app.db.database import async_main
from app.handlers.task import task_router
from app.handlers.user import user_router


async def main():
    await async_main()
    
    load_dotenv()

    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(task_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')