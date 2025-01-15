from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import StatesGroup, State

from environs import Env


class ConfigBot:
    def __init__(self):

        env = Env()
        env.read_env()

        self.STOR = MemoryStorage()

        self.TOKEN: str = env.str("TOKEN")

        self.bot: Bot = Bot(self.TOKEN)
        self.dp: Dispatcher = Dispatcher(storage=self.STOR)

        self.URL_BOT: str = env.str("URL_BOT")
        admin_id = env.str("ADMINS_ID").replace(" ", "")
        self.ADMINS_ID: list = list(map(int, admin_id.split(",")))

    async def skip_updates(self):
        try:
            await self.bot.delete_webhook(drop_pending_updates=True)
        except:
            pass


class states(StatesGroup):
    _ = State()

