from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from logic.keyboards.menu_key import variants_keyboard, menu_keyboard
from logic.status.Status import SurveyStates
from logic.user.open_questions import start_open_questions, ask_open_question

router = Router()


async def ask_1_to_5_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_index = data["current_question_index"]
    questions = data["questions_1_to_5"]

    if question_index < len(questions):
        show_back = question_index > 0
        await message.answer(
            text=f"❔ {questions[question_index]}\n\n⭐️ Оцените от 1 до 5:",
            reply_markup=variants_keyboard(with_back=show_back)
        )
        await state.set_state(SurveyStates.QUESTIONS_1_TO_5)
    else:
        await start_open_questions(message, state)


@router.callback_query(SurveyStates.QUESTIONS_1_TO_5, F.data.startswith("answer_1_to_5:"))
async def process_1_to_5_answer(call: types.CallbackQuery, state: FSMContext):
    answer = int(call.data.split(":")[1])
    data = await state.get_data()

    # Сохраняем текущий ответ в историю
    question_index = data["current_question_index"]
    question_text = data["questions_1_to_5"][question_index]
    previous_answers = data.get("previous_answers", [])
    previous_answers.append({
        "index": question_index,
        "question": question_text,
        "answer": answer
    })

    # Обновляем состояние
    await state.update_data(
        answers_1_to_5={**data["answers_1_to_5"], question_text: answer},
        current_question_index=question_index + 1,
        previous_answers=previous_answers
    )

    await call.message.delete()
    await ask_1_to_5_question(call.message, state)
