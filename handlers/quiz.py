from aiogram import Router, types, F
from aiogram.filters.command import Command
from utils.gpt_service import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.prof_keyboard import make_row_kayboard

router = Router()
gpt_service = ChatGPTService()

topics = {'nature', 'science', 'sport', 'films'}


class ChatGPTState(StatesGroup):
    waiting_for_topic = State()
    waiting_for_quiz_prompt = State()


# /quiz - Начало викторины
@router.message(Command('quiz'))
async def quiz_init(message: types.Message, state: FSMContext):
    await message.answer_photo(types.FSInputFile('assets/quiz.png'))
    await message.answer(f'{message.chat.first_name}! Choose a topic to start the quiz:',
                         reply_markup=make_row_kayboard(topics))

    await state.update_data(correct_answers=0, selected_topic=None)

    await state.set_state(ChatGPTState.waiting_for_topic)


@router.message(F.text == 'Change topic')
async def quiz_change_topic(message: types.Message, state: FSMContext):
    await state.update_data(selected_topic=None)

    await message.answer("Choose a new topic:", reply_markup=make_row_kayboard(topics))
    await state.set_state(ChatGPTState.waiting_for_topic)


@router.message(ChatGPTState.waiting_for_topic, F.text.in_(topics))
async def quiz_start_topic(message: types.Message, state: FSMContext):
    topic = message.text
    await state.update_data(selected_topic=topic)

    gpt_service.set_system_message(f'This is a quiz about "{topic}". '
                                   f'You need to ask one question on this topic and check if the answer is correct. '
                                   f'If the answer is wrong, provide the correct one.')

    await message.answer(f'You chose "{topic}". Generating your first question...')

    await ask_new_question(message, state)


@router.message(F.text == 'Next question')
async def quiz_next_question(message: types.Message, state: FSMContext):
    await ask_new_question(message, state)


@router.message(ChatGPTState.waiting_for_quiz_prompt)
async def quiz_check_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    selected_topic = data.get("selected_topic")

    if not selected_topic:
        await message.answer("Error: No topic selected. Please restart the quiz.")
        return

    gpt_service.add_user_message(f'My answer is: {message.text}. Is it correct? Answer only "yes" or "no".')
    response = gpt_service.get_response().strip().lower()

    correct_answers = data.get("correct_answers", 0)

    if "yes" in response:
        correct_answers += 1
        await state.update_data(correct_answers=correct_answers)
        result_message = f"✅ Correct! Your score: {correct_answers} 🎉"
    else:
        gpt_service.add_user_message(f"What is the correct answer to the last question?")
        correct_answer = gpt_service.get_response()

        result_message = f"❌ Incorrect. {correct_answer}\nYour score: {correct_answers}"

    await message.answer(f"{result_message}\n\nNext action?",
                         reply_markup=make_row_kayboard({'Next question', 'Change topic', 'Enough'}))


async def ask_new_question(message: types.Message, state: FSMContext):
    """Генерирует новый вопрос на основе сохранённой темы"""
    data = await state.get_data()
    selected_topic = data.get("selected_topic")

    if not selected_topic:
        await message.answer("Error: No topic selected. Please restart the quiz.")
        return

    gpt_service.set_system_message(f'This is a quiz about "{selected_topic}". '
                                   f'You need to ask one question on this topic and check if the answer is correct. '
                                   f'If the answer is wrong, provide the correct one.')

    response = gpt_service.get_response()

    await message.answer(f'Next question on "{selected_topic}":\n{response}\nYour answer: ',
                         reply_markup=make_row_kayboard({''}))

    await state.set_state(ChatGPTState.waiting_for_quiz_prompt)