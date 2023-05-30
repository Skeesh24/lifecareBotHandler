

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from bot import web_app


Plugin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="LIFE", web_app=web_app)]
    ],
    resize_keyboard=True
)


cb = CallbackData('btn', 'action')
key = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton('PAY', callback_data='btn:buy')]]
)
