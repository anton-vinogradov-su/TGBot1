from aiogram import Router, types, F
from aiogram.filters.command import Command
from utils.gpt_service import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.prof_keyboard import make_row_kayboard

router = Router()

gpt_service = ChatGPTService()


# gpt_service.set_system_message('Ты лучший hr-менеджер. Задавай профильные вопросы для соискателей')

# class ChatGPTState(StatesGroup):
#     waiting_for_prompt = State()


# /quiz
@router.message(Command('quiz'))
async def quiz_init(message: types.Message):
    await message.answer_photo(types.FSInputFile('assets/quiz.png'))
