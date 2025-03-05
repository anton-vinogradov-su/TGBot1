import config
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio

TOKEN_API = config.TG_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_API)
dp = Dispatcher()


# /start
@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.reply("Привет! Это простой бот, который отвечает на вопросы о музыке.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
