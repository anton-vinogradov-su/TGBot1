from aiogram import Router, types, F
from aiogram.filters.command import Command
from utils.gpt_service import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

gpt_service = ChatGPTService()


# make common
class ChatGPTState(StatesGroup):
    waiting_for_common_chatgpt_prompt = State()


# /chatgpt
@router.message(Command('chatgpt'))
async def command_gpt(message: types.Message, state: FSMContext):
    await message.answer_photo(types.FSInputFile('assets/chatgpt.webp'))
    await message.answer(f'{message.chat.first_name}! Введи свой запрос ChatGPT:')
    await state.set_state(ChatGPTState.waiting_for_common_chatgpt_prompt)


@router.message(ChatGPTState.waiting_for_common_chatgpt_prompt)
async def gpt_chatgpt_answer(message: types.Message, state: FSMContext):
    gpt_service.add_user_message(message.text)
    response = gpt_service.get_response()
    await message.answer(response)
    await state.clear()
