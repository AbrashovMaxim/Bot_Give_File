from aiogram import Bot, types, F, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, inline_keyboard_button, ChatMemberUpdated
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.enums import ParseMode
from aiogram.enums.content_type import ContentType
import asyncio

# -1002090514593 - ТИХО
# -1001939405814 - Мульт
# -1001775771244 - Сериал
# -1001779666110 - Кино

from libs.other import router
from libs.config import config

async def main():
    bot = Bot(token=config.get_token(), parse_mode="HTML")
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
