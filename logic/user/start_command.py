from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from logic.keyboards.menu_key import menu_keyboard, admin_menu
from logic.config import ADMIN_ID
router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if user_id == ADMIN_ID:
        await message.answer("👋 Привет, Админ!", reply_markup= admin_menu())
    else:
        await message.answer(f"👋 Привет, {user_name}!\n\n✍️ Выберите действие:",
                             reply_markup=menu_keyboard())


@router.message()
async def text_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.answer("👋 Привет, Админ!", reply_markup= admin_menu())
    else:
        await message.answer("✍️ Выберите действие:", reply_markup=menu_keyboard())
