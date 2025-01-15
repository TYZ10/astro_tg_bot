from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import StatesGroup, State

from environs import Env


class ConfigBot:
    def __init__(self, token: str, url_bot: str):

        env = Env()
        env.read_env()

        self.STOR = MemoryStorage()

        self.TOKEN: str = token

        self.bot: Bot = Bot(self.TOKEN)
        self.dp: Dispatcher = Dispatcher(storage=self.STOR)

        self.URL_BOT = url_bot
        self.ADMIN_ID = [2030444507]

    async def skip_updates(self):
        try:
            await self.bot.delete_webhook(drop_pending_updates=True)
        except:
            pass


class states(StatesGroup):
    _ = State()

