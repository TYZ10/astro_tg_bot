from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation
from .get_info_gpt import main_get_info_gpt
from ...misc import create_aspects


class AnalyzingPersonalStrengths(BasicBotOperation):

    text = "Ты профессиональный астролог. На основе данных о дате, времени и месте рождения составь подробный анализ сильных сторон личности. Используй следующую структуру: 1) Введение — цель анализа и его значимость для самопознания. 3) Карта сильных сторон — раздели на личностные качества, социальные таланты, творческий и духовный потенциал 3) Интеллектуальные способности — сильные стороны в обучении, коммуникации и принятии решений. 4) Эмоциональная устойчивость — как человек справляется с трудностями, на что опирается. 5) Социальная адаптация — особенности взаимодействия с окружающими и построения связей. 6) Лидерские и творческие способности — возможности вдохновлять и создавать новое.  7) Путь героя — как сильные стороны развиваются через вызовы и успехи, 8 Рекомендации — как развивать свои сильные стороны для достижения успеха. 9) Заключение — ключевые выводы и практические советы для дальнейшего роста. Не используй термины астрологии, такие как знаки зодиака, названия планет или аспектов, но сохраняй суть их взаимодействия и влияния на разные сферы жизни."

    async def analyzing_personal_strengths(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ):
        await call.message.answer("""🌌 Что делает тебя уникальным? Твой анализ сильных сторон покажет, в чём твоя сила и как её использовать для достижения целей. Ты узнаешь:
✨ Какие качества помогают тебе двигаться вперёд.
💪 Как справляться с трудностями, используя свои ресурсы.
🌟 Как твоя личность влияет на отношения, карьеру и жизнь.

Этот анализ поможет глубже понять себя и свои возможности. Жми кнопку и начни своё путешествие к самопознанию! 🚀""")

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
            self.analyzing_personal_strengths,
            F.data == "start generation",
            StateFilter(AllTypesGeneration.analyzing_personal_strengths.state)
        )
