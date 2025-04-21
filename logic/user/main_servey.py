from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from logic.questions import QUESTIONS
from logic.status.Status import SurveyStates
from logic.user.number_servey import ask_1_to_5_question
from logic.user.open_questions import ask_open_question

router = Router()


@router.callback_query(F.data.startswith("poll:"))
async def start_poll(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    poll_name = call.data.split(":")[1]
    survey = QUESTIONS[poll_name]

    if "1_to_5" not in survey:
        open_questions = survey["open"]

        await state.update_data(
            current_poll=poll_name,
            open_questions=open_questions,
            current_open_question_index=0,
            open_answers={}
        )

        await ask_open_question(call.message, state)
    else:
        await state.update_data(
            current_poll=poll_name,
            questions_1_to_5=survey["1_to_5"],
            current_question_index=0,
            answers_1_to_5={},
            previous_answers=[]
        )
        await ask_1_to_5_question(call.message, state)

    await call.bot.answer_callback_query(call.id, text="", show_alert=False)


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


