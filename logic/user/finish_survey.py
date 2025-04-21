from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from logic.keyboards.menu_key import variants_keyboard, menu_keyboard
from logic.user.save_to_excel import save_to_excel


async def finish_survey(message: types.Message, state: FSMContext):
    data = await state.get_data()

    username = message.from_user.full_name

    all_answers = {
        "1_to_5_answers": data.get("answers_1_to_5", {}),
        "open_answers": data.get("open_answers", {})
    }

    await save_to_excel(
        all_answers=all_answers,
        username=username,
        poll_name=data["current_poll"]
    )

    await message.answer(
        "🔥 Спасибо за прохождение опроса!\n",
        reply_markup=menu_keyboard()
    )

    await state.clear()
