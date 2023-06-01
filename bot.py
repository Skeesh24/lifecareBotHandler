from aiogram import Bot, Dispatcher
from aiogram.types import WebAppInfo
from config import Config
import asyncio


bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(bot=bot)
web_app = WebAppInfo(url="https://skeesh24.github.io/plugbot/")


async def main() -> None:
    from handlers import dp
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('bot was stopped...')
