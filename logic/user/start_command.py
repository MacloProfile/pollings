import re

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from logic.keyboards.menu_key import menu_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user_name = message.from_user.first_name
    await message.answer(f"👋 Привет, {user_name}!\n\n✍️ Выберите действие:",
                         reply_markup=menu_keyboard())
