from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from logic.questions import QUESTIONS
from logic.status.Status import SurveyStates
from logic.user.finish_survey import finish_survey

router = Router()


async def start_open_questions(message: types.Message, state: FSMContext):
    data = await state.get_data()
    survey = QUESTIONS[data["current_poll"]]
    open_questions = survey["open"]

    await state.update_data(
        open_questions=open_questions,
        current_open_question_index=0,
        open_answers={}
    )

    await ask_open_question(message, state)


async def ask_open_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_index = data["current_open_question_index"]
    questions = data["open_questions"]

    if question_index < len(questions):
        await message.answer(questions[question_index])
        await state.set_state(SurveyStates.OPEN_QUESTIONS)
    else:
        # Все вопросы заданы, завершаем опрос
        await finish_survey(message, state)


@router.message(SurveyStates.OPEN_QUESTIONS)
async def process_open_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_index = data["current_open_question_index"]
    question_text = data["open_questions"][question_index]
    answers = data.get("open_answers", {})

    # Сохраняем ответ
    answers[question_text] = message.text

    # Обновляем состояние
    await state.update_data(
        open_answers=answers,
        current_open_question_index=question_index + 1
    )

    await ask_open_question(message, state)
