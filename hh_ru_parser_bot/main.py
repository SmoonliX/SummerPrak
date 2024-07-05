from aiogram import Bot, Dispatcher
import asyncio
from app.handlers.handlers_resume import router as r1
from app.handlers.handlers_vacancy import router as r2
import os
from dotenv import load_dotenv
from database.models import async_main


async def main():
    load_dotenv()
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(r1)
    dp.include_router(r2)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
