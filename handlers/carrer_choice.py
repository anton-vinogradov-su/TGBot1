from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.prof_keyboard import make_row_kayboard

router = Router()

availablie_jobs = [
    'Software developer',
    'Manager',
    'Designer',
    'Marketing specialist',
]

availablie_grades = [
    'Junior',
    'Middle',
    'Senior',
]


class CarrerChoice(StatesGroup):
    job = State()
    grade = State()


@router.message(Command('prof'))
async def command_prof(message: types.Message, state: FSMContext):
    await message.answer('Occupation: ', reply_markup=make_row_kayboard(availablie_jobs))
    await state.set_state(CarrerChoice.job)


@router.message(CarrerChoice.job, F.text.in_(availablie_jobs))
async def prof_chosen(message: types.Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await message.answer('Level: ', reply_markup=make_row_kayboard(availablie_grades))
    await state.set_state(CarrerChoice.grade)


@router.message(CarrerChoice.job)
async def prof_incorrect(message: types.Message, state: FSMContext):
    await message.answer('Occupation again: ', reply_markup=make_row_kayboard(availablie_jobs))
#    await state.set_state(CarrerChoice.job)


@router.message(CarrerChoice.grade, F.text.in_(availablie_grades))
async def prof_chosen1(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f'Your occupation: {user_data["profession"]}, level: {message.text}',
                         reply_markup=make_row_kayboard(availablie_grades))
    await state.clear()


@router.message(CarrerChoice.grade)
async def grade_incorrect(message: types.Message, state: FSMContext):
    await message.answer('Level again: ', reply_markup=make_row_kayboard(availablie_grades))
#    await state.set_state(CarrerChoice.grade)
