from aiogram import Router, types, F
from aiogram.filters.command import Command
from keyboards.prof_keyboard import make_row_kayboard
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()

# /random
@router.message(F.text == 'Хочу ещё факт')
@router.message(Command('random'))
async def random(message: types.Message):
    await message.answer_photo(types.FSInputFile('assets/random_fact.png'))
    gpt_service.add_user_message("Пришли какой-нибудь интересный случайный факт о программировании.")
    response = gpt_service.get_response()
    await message.answer(response, reply_markup=make_row_kayboard({'Закончить', 'Хочу ещё факт'}))
