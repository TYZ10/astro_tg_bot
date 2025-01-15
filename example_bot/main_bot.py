import asyncio

from aiogram import Bot
from aiogram.types import BotCommand

from .Config_bot import ConfigBot


class TelegramBot:
    def __init__(self):
        self.config = ConfigBot()

    async def __create_bot(self):
        await self.config.skip_updates()

    async def start_bot(self):
        await self.__create_bot()

        try:
            await self.config.dp.start_polling(self.config.bot)
        except Exception as e:
            print(e)



