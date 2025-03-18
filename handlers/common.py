import random
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.randomfox import fox
from keyboards.keyboards import kb1, kb2
from handlers.inline_handlers import router as inline_router

router = Router()
router.include_routers(inline_router)


# /start
@router.message(F.text == 'Закончить')
@router.message(Command('start'))
async def start_command(message: types.Message):
    await message.reply(f'Привет, {message.chat.first_name}! Это простой бот.', reply_markup=kb1)


@router.message(Command('ura'))
async def ura_command(message: types.Message):
    await message.reply(f'Ура! {message.chat.first_name}! Hello World', reply_markup=kb2)


@router.message(Command('fox'))
async def fox_command(message: types.Message):
    image_fox = fox()
    await message.answer_photo(image_fox)


@router.message(F.text.lower() == 'num')
async def number_command(message: types.Message):
    number = random.randint(1, 100)
    await message.answer(f'Ok, your number is {number}')


# default router
@router.message()
async def default_echo(message: types.Message):
    await message.answer("Unknown command. Try again.")
