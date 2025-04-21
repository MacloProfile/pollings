from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from logic.questions import QUESTIONS


def menu_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in QUESTIONS.keys():
        keyboard.button(text=f"📊 {key}", callback_data=f"poll:{key}")
    keyboard.adjust(1)
    return keyboard.as_markup()


def variants_keyboard(with_back=False):
    buttons = [
        [types.InlineKeyboardButton(text=str(i), callback_data=f"answer_1_to_5:{i}")]
        for i in range(1, 6)
    ]
    if with_back:
        buttons.append([types.InlineKeyboardButton(text="← Назад", callback_data="back_1_to_5")])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def cancel_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Назад", callback_data="cancel_distribution")
    return keyboard.as_markup()

