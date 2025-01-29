from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation
from .get_info_gpt import main_get_info_gpt
from ...misc import create_aspects


class RecommendationsActualization(BasicBotOperation):

    text = 'Ты профессиональный астролог. На основе данных о дате, времени и месте рождения составь рекомендации по самореализации. Используй следующую структуру: 1) Введение — зачем важно раскрыть свой потенциал и достичь самореализации. 2) Ключевые таланты — способности, которые помогут человеку найти своё предназначение. 3) Возможности для роста — направления, которые откроют наибольший потенциал. 4) Вызовы и препятствия — как справляться с трудностями на пути к самореализации. 5) Поддерживающие факторы — что помогает человеку достигать целей и сохранять баланс. 6) Идеальные сферы деятельности — профессии и увлечения, которые принесут удовлетворение. 7) Рекомендации — шаги для гармоничного соединения личных целей с внешними обстоятельствами. 8) Заключение — ключевые выводы и практические советы для достижения гармонии и успеха. Не используй термины астрологии, такие как знаки зодиака, названия планет или аспектов, но сохраняй суть их взаимодействия и влияния на разные сферы жизни.'

    async def recommendations_actualization(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ):
        await call.message.answer("""🌟 Хочешь узнать, как лучше развивать свои таланты, находить гармонию и двигаться к своей цели? Рекомендации по саморазвитию на основе твоих астрологических данных помогут тебе:
✨ Раскрыть скрытые способности.
💡 Понять, как реализовать свой потенциал.
🚀 Найти вдохновение для новых шагов.

Каждый человек уникален, и звёзды подскажут, как лучше раскрыть твою индивидуальность. 💫""")

        col_info = self.operation_db.COLUMNS_INFO

        (place_birth, latitude, longitude, time_birth,
         data_birth) = self.operation_db.select_user_info_db(
            f"{col_info.place_birth}, "
            f"{col_info.latitude}, "
            f"{col_info.longitude}, "
            f"{col_info.time_birth}, "
            f"{col_info.data_birth}",
            call.from_user.id,
            many=True
        )

        aspects = create_aspects(
            f"{data_birth} {time_birth}",
            latitude,
            longitude
        )

        text_gpt = await main_get_info_gpt(
            self.config,
            f"{data_birth}, {time_birth}, {place_birth} \n\n{aspects}",
            self.text
        )
        (count_generation,
         generation_count_all) = self.operation_db.select_user_info_db(
            f"{self.operation_db.COLUMNS_INFO.generation_count}, "
            f"{self.operation_db.COLUMNS_INFO.generation_count_all}",
            call.from_user.id,
            many=True
        )

        self.operation_db.update_user_info_db(
            {
                self.operation_db.COLUMNS_INFO.generation_count: count_generation - 1,
                self.operation_db.COLUMNS_INFO.generation_count_all: generation_count_all + 1,
            },
            call.from_user.id
        )

        await call.message.answer(
            text=str(text_gpt)
        )

        await call.message.answer(
            text=f"Количество оставшихся генераций: {count_generation - 1}",
            reply_markup=self.keyboard.main_menu_kb
        )

        await state.clear()

    def create_router(self):
        self.router.callback_query.register(
            self.recommendations_actualization,
            F.data == "start generation",
            StateFilter(
                AllTypesGeneration.recommendations_self_actualization.state
            )
        )
