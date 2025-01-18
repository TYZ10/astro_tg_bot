from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import StatesGroup, State

from environs import Env
from opencage.geocoder import OpenCageGeocode


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
        self.CHANEL_URL: str = env.str("CHANEL_URL")
        self.CHANEL_ID: int = env.int("CHANEL_ID")

        self.POSTGRESQL_USER: str = env.str("POSTGRESQL_USER")
        self.POSTGRESQL_PASSWORD: str = env.str("POSTGRESQL_PASSWORD")
        self.POSTGRESQL_DBNAME: str = env.str("POSTGRESQL_DBNAME")

        #https://opencagedata.com/api
        location_api_key: str = env.str("LOCATION_API_KEY")
        self.geocoder: OpenCageGeocode = OpenCageGeocode(location_api_key)

    async def skip_updates(self):
        try:
            await self.bot.delete_webhook(drop_pending_updates=True)
        except:
            pass


class states(StatesGroup):
    data_birth = State()
    time_birth = State()
    place_birth = State()
