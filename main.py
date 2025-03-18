from aiogram.exceptions import TelegramAPIError
import config
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import common, talk, quiz, gpt_chat, random_fact, translation, image


async def main():
    TOKEN_API = config.TOKEN_TG

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN_API)
    dp = Dispatcher()
    storage = MemoryStorage()

    dp.include_router(random_fact.router)
    dp.include_router(gpt_chat.router)
    dp.include_router(talk.router)
    dp.include_router(quiz.router)
    dp.include_router(translation.router)
    dp.include_router(image.router)
    dp.include_router(common.router)

    #    dp.include_router(carrer_choice.router)

    while True:
        try:
            await dp.start_polling(bot)
        except TelegramAPIError as e:
            print(f"Error: {e}. Restarting bot...")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())
