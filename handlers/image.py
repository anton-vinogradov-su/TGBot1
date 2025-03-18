from io import BytesIO
import aiohttp
from aiogram import Router, types, F
from aiogram.filters.command import Command
from keyboards.keyboards import kb1, kb2
from utils.gpt_service import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()
gpt_service = ChatGPTService()


# make common
class ChatGPTState(StatesGroup):
    waiting_for_image = State()


# /image
@router.message(Command('image'))
async def image_init(message: types.Message, state: FSMContext):
    await message.answer(f'{message.chat.first_name}! Share your image:',
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ChatGPTState.waiting_for_image)


@router.message(ChatGPTState.waiting_for_image, F.photo)
async def image_do(message: types.Message, state: FSMContext, bot):
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"

    async with (aiohttp.ClientSession() as session):
        async with session.get(file_url) as resp:
            if resp.status == 200:
                image_bytes = await resp.read()
                image_stream = BytesIO(image_bytes)

                # Отправляем изображение в GPT-4
                response = await gpt_service.analyze_image(image_stream)

                await message.answer(f"💬 {response}", reply_markup=kb1)
                await state.clear()
            else:
                await message.answer("❌ Failed to download the image. Please try again.")
