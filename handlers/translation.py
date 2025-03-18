from aiogram import Router, types, F
from aiogram.filters.command import Command
from utils.gpt_service import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.prof_keyboard import make_row_kayboard

router = Router()
gpt_service = ChatGPTService()

# make common
class ChatGPTState(StatesGroup):
    waiting_for_text = State()
    waiting_for_celebrity_prompt = State()


# /translation
@router.message(Command('translation'))
async def translation_init(message: types.Message, state: FSMContext):
    await message.answer(f'{message.chat.first_name}! Enter text for translation:', reply_markup=make_row_kayboard({''}))
    await state.set_state(ChatGPTState.waiting_for_text)


@router.message(ChatGPTState.waiting_for_text)
async def translation_do(message: types.Message, state: FSMContext):
    gpt_service.add_user_message('Detect source language and translate following text into English:\n' + message.text)
    response = gpt_service.get_response()
    await message.answer(f"💬 {response}")
