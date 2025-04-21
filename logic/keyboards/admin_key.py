from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


# /admin
def admin_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Рассылка", callback_data="distribution")
    return keyboard.as_markup()


# /back
def back_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Назад", callback_data="cancel_distribution")
    return keyboard.as_markup()


def send_ad_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text="Отправить Рассылку", callback_data="advertisement_send"))
    return keyboard.as_markup()