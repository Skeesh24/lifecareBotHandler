from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import web_app

from config import Config

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            'Profile', callback_data=Config.PROFILE_DATA),
         InlineKeyboardButton('Why', callback_data=Config.WHY_DATA)]
    ],
)

why_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            'Назад', callback_data=Config.WHYBACK_DATA)]
    ],
)

profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            'Buy LIFE sub', web_app=web_app),
         InlineKeyboardButton('Назад', callback_data=Config.PROFILEBACK_DATA)]
    ],
)
