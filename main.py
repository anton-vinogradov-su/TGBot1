import config
import logging
from aiogram import Bot, Dispatcher, types, F
import asyncio
from handlers import common, carrer_choice

async def main():
    TOKEN_API = config.TG_TOKEN

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN_API)
    dp = Dispatcher()

    dp.include_router(carrer_choice.router)
    dp.include_router(common.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
