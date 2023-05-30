from aiogram.types import LabeledPrice, Message, PreCheckoutQuery, ContentType
from bot import bot, dp
from aiogram.dispatcher.filters import Command
from config import Config
from keyboards.plugin_keyboard import Plugin_keyboard

prices = {
    'standart': LabeledPrice(label='Standart', amount=43200),
    'xtra': LabeledPrice(label='Xtra', amount=84700),
    'premium': LabeledPrice(label='Premium', amount=101700)
}


@dp.message_handler(Command('start'))
async def start(message: Message):
    await bot.send_message(message.chat.id, f"Hola. {prices['1']}", reply_markup=Plugin_keyboard)


@dp.message_handler(content_types='web_app_data')
async def buy_process(resp: Message):
    await bot.send_invoice(resp.chat.id,
                           title='standart',
                           description='standart service pack',
                           provider_token=Config.PAYMENTS_TOKEN,
                           currency='rub',
                           need_email=True,
                           prices=prices[f'{resp.web_app_data.data}'],
                           start_parameter='example',
                           payload='some_invoice')


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_process(pre_checkout: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await bot.send_message(message.chat.id, "Payment successful!")


@dp.message_handler(content_types=ContentType.STICKER)
async def sticker_sent(message: Message):
    await bot.send_message(message.chat.id, "Не надо мне вот эти твои стикиры")
