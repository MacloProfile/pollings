from aiogram.fsm.state import StatesGroup, State


class SurveyStates(StatesGroup):
    WAITING_FOR_ANSWER = State()
    QUESTIONS_1_TO_5 = State()
    OPEN_QUESTIONS = State()