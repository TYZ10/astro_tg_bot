import asyncio

from aiogram import Bot
from aiogram.types import BotCommand

from .Config_bot import ConfigBot


class TelegramBot:
    def __init__(self, token: str, url_bot: str, lang: str,
                 curency_symbol: str,get_start_bonus_money: int,
                 name_db: str, technical_support: str,
                 instruction_text: str,
                 feedback_channel: list,
                 news_channel: list):
        self.token = token
        self.url_bot = url_bot

        self.lang = lang
        self.curency_symbol = curency_symbol
        self.get_start_bonus_money = get_start_bonus_money
        self.technical_support = technical_support
        self.instruction_text = instruction_text
        self.name_db = name_db

        self.feedback_channel = feedback_channel
        self.news_channel = news_channel

    async def __create_bot(self):
        self.config = ConfigBot(token=self.token,
                                url_bot=self.url_bot)

        await self.config.skip_updates()


    async def start_bot(self):
        await self.__create_bot()

        try:
            await self.config.dp.start_polling(self.config.bot)
        except Exception as e:
            print(e)



