import asyncio
from aiogram import Bot, Dispatcher
from core.config import BOT_TOKEN
from handlers import common, chat
import traceback
import time


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(common.router)
dp.include_router(chat.router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print(f"{'Run':>22}")
    while True:
        try:
            asyncio.run(main())
        except Exception:
            print(f"[ERROR main loop] {traceback.format_exc()}")
        finally:
            asyncio.run(bot.session.close())

        time.sleep(5)