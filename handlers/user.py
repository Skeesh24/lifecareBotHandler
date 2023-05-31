from typing import Any
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery, ContentType, CallbackQuery
from bot import bot, dp
from aiogram.dispatcher.filters import Command
from config import Config
from keyboards.profile_keyboard import start_keyboard, why_keyboard, profile_keyboard


prices = {
    'standart': LabeledPrice(label='Standart', amount=43200),
    'xtra': LabeledPrice(label='Xtra', amount=84700),
    'premium': LabeledPrice(label='Premium', amount=101700)
}


@dp.message_handler(Command('start'))
async def start(message: Message):
    await bot.send_message(
        message.chat.id,
        Config.START_MESSAGE,
        reply_markup=start_keyboard)


@dp.message_handler(content_types='web_app_data')
async def buy_process(resp: Message):
    await bot.send_invoice(resp.chat.id,
                           title=prices[f'{resp.web_app_data.data}'].label,
                           description=f'{prices[f"{resp.web_app_data.data}"].label} service pack',
                           provider_token=Config.PAYMENTS_TOKEN,
                           currency='rub',
                           need_email=True,
                           prices=[prices[f'{resp.web_app_data.data}']],
                           start_parameter='example',
                           payload='some_invoice')


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_process(pre_checkout: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await bot.send_message(message.chat.id, Config.PAYMENT_ANSWER)


@dp.message_handler(content_types=ContentType.STICKER)
async def sticker_sent(message: Message):
    await bot.send_message(message.chat.id, Config.STICKER_ANSWER)


@dp.callback_query_handler()
async def query_handler(callback: CallbackQuery):
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

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=markup,
        text=text)


def getProfileAnswer(message: Message) -> str:
    return f'Hello, {message.chat.username}.\n'\
        f'this is ur profile.'
