import random
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.randomfox import fox
from keyboards.keyboards import kb1, kb2
from keyboards.inline_kb import inline_keyboard
from handlers.inline_handlers import router as inline_router

router = Router()
router.include_routers(inline_router)


# /start
@router.message(Command('start'))
async def start_command(message: types.Message):
    await message.reply(f'Привет, {message.chat.first_name}! Это простой бот.', reply_markup=kb1)
    await message.answer(f'{message.chat.first_name} нажми и задай вопрос!', reply_markup=inline_keyboard)


@router.message(Command('ura'))
async def start_command(message: types.Message):
    await message.reply(f'Ура! {message.chat.first_name}! Hello World', reply_markup=kb2)


@router.message(Command('fox'))
async def start_command(message: types.Message):
    image_fox = fox()
    await message.answer_photo(image_fox)

@router.message(F.text.lower() == 'num')
async def start_number(message: types.Message):
    number = random.randint(1, 100)
    await message.answer(f'Ok, your number is {number}')


# @router.message(F.text)
# async def echo(message: types.Message):
#     await message.answer(message.text)
