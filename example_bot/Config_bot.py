from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import StatesGroup, State

from openai import AsyncOpenAI
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
        self.CHANEL_ID: str = env.str("CHANEL_ID")

        self.POSTGRESQL_USER: str = env.str("POSTGRESQL_USER")
        self.POSTGRESQL_PASSWORD: str = env.str("POSTGRESQL_PASSWORD")
        self.POSTGRESQL_DBNAME: str = env.str("POSTGRESQL_DBNAME")
        self.POSTGRESQL_TABLE_NAME: str = env.str("POSTGRESQL_TABLE_NAME")

        #https://opencagedata.com/api
        location_api_key: str = env.str("LOCATION_API_KEY")
        self.geocoder: OpenCageGeocode = OpenCageGeocode(location_api_key)

        TOKEN_CHAT_GPT: str = env.str("TOKEN_CHAT_GPT")

        self.client_gpt: AsyncOpenAI = AsyncOpenAI(
            api_key=TOKEN_CHAT_GPT
        )
        self.store_id = env.int("STORE_ID")
        self.the_secret_key = env.str("THE_SECRET_KEY")

    async def skip_updates(self):
        try:
            await self.bot.delete_webhook(drop_pending_updates=True)
        except:
            pass


class states(StatesGroup):
    data_birth = State()
    time_birth = State()
    place_birth = State()

    natal_chart_analysis = State()
    natal_chart_analysis_1_aspect = State()
    natal_chart_analysis_2_aspect = State()

    predictions = State()
    predictions_1_aspect = State()
    predictions_2_aspect = State()

    horoscope_for_business = State()
    recommendations_self_actualization = State()
    analyzing_compatibility_relationship = State()
    astrological_forecast_health = State()
    analyzing_personal_strengths = State()

    set_time_prediction = State()
