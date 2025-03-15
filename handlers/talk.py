from aiogram import Router, types, F
from aiogram.filters.command import Command
from utils.gpt_service import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.prof_keyboard import make_row_kayboard

router = Router()
gpt_service = ChatGPTService()

celebrities = {'Джон Леннон',
               'Клинт Иствуд',
               'Альберт Эйнштейн',
               'Джоан Роулинг',
               }


# make common
class ChatGPTState(StatesGroup):
    waiting_for_celebrity = State()  # Состояние для выбора персонажа
    waiting_for_celebrity_prompt = State()  # Состояние для ожидания вопроса


# /talk - начало диалога
@router.message(Command('talk'))
async def talk_init(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer_photo(types.FSInputFile('assets/celebrity.png'))
    await message.answer(f'{message.chat.first_name}! Выбери известную личность для общения:',
                         reply_markup=make_row_kayboard(celebrities))
    await state.set_state(ChatGPTState.waiting_for_celebrity)


@router.message(ChatGPTState.waiting_for_celebrity,
                F.text.in_(celebrities))
async def talk_set_celebrity(message: types.Message, state: FSMContext):
    character = message.text
    await state.update_data(selected_character=character)
    gpt_service.set_system_message(f'Ты {character}. Отвечай в стиле этого персонажа.')
    await message.answer(f'Ты выбрал {character}. Задай свой вопрос: ')
    await state.set_state(ChatGPTState.waiting_for_celebrity_prompt)


@router.message(ChatGPTState.waiting_for_celebrity_prompt)
async def talk_chatgpt_answer(message: types.Message, state: FSMContext):
    gpt_service.add_user_message(message.text)
    response = gpt_service.get_response()
    await message.answer(f"💬 {response}", reply_markup=make_row_kayboard({'Закончить'}))
    await state.clear()
