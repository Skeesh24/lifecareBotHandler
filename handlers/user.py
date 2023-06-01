from typing import Any
from aiogram.types import Message, PreCheckoutQuery, ContentType, CallbackQuery
from bot import bot, dp
from aiogram.dispatcher.filters import Command
from config import Config
from keyboards.profile_keyboard import start_keyboard, why_keyboard, profile_keyboard
from keyboards.plugin_keyboard import plugin_keyboard
from services.database import db
from services.subscriptions import getSubFromCallbackData


@dp.message_handler(Command('start'))
async def start(message: Message) -> None:
    await bot.send_message(
        message.chat.id,
        Config.START_MESSAGE,
        reply_markup=start_keyboard)


@dp.message_handler(content_types='web_app_data')
async def buy_process(resp: Message) -> None:
    data = resp.web_app_data.data
    await bot.send_invoice(resp.chat.id,
                           title=getSubFromCallbackData(db, f'{data}').label,
                           description=f'{getSubFromCallbackData(db, f"{data}").label} service pack',
                           provider_token=Config.PAYMENTS_TOKEN,
                           currency='rub',
                           need_email=True,
                           prices=[getSubFromCallbackData(db, f'{data}')],
                           start_parameter='example',
                           payload='some_invoice')


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_process(pre_checkout: PreCheckoutQuery) -> None:
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message) -> None:
    await bot.send_message(message.chat.id, Config.PAYMENT_ANSWER)


@dp.message_handler(content_types=ContentType.STICKER)
async def sticker_sent(message: Message) -> None:
    await bot.send_message(message.chat.id, Config.STICKER_ANSWER)


@dp.callback_query_handler()
async def query_handler(callback: CallbackQuery) -> None:
    markup: Any
    text = ""

    match callback.data:
        case Config.PROFILE_DATA:
            markup = profile_keyboard
            text = getProfileAnswer(callback.message)
        case Config.WHY_DATA:
            markup = why_keyboard
            text = Config.WHY_ANSWER
        case Config.WHYBACK_DATA:
            markup = start_keyboard
            text = Config.START_MESSAGE
        case Config.PROFILEBACK_DATA:
            markup = start_keyboard
            text = Config.START_MESSAGE
        case Config.BUY_DATA:
            await bot.send_message(
                callback.message.chat.id,
                Config.BUY_ANSWER,
                reply_markup=plugin_keyboard)
            return

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=markup,
        text=text)


# remove in most likely unit, stop to store it with dp handlers
def getProfileAnswer(message: Message) -> str:
    return f'Hello, {message.chat.username}.\n'\
        f'this is ur profile.'
