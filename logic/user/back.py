from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from logic.status.Status import SurveyStates
from logic.user.number_servey import ask_1_to_5_question

router = Router()


@router.callback_query(SurveyStates.QUESTIONS_1_TO_5, F.data == "back_1_to_5")
async def back_to_previous_question(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    previous_answers = data.get("previous_answers", [])

    if not previous_answers:
        await call.answer("Это первый вопрос, нельзя вернуться назад")
        return

    # Получаем последний ответ
    last_answer = previous_answers.pop()

    # Удаляем последний ответ из сохраненных
    answers = data["answers_1_to_5"]
    if last_answer["question"] in answers:
        del answers[last_answer["question"]]

    # Обновляем состояние
    await state.update_data(
        current_question_index=last_answer["index"],
        answers_1_to_5=answers,
        previous_answers=previous_answers
    )

    await call.message.delete()
    await ask_1_to_5_question(call.message, state)


