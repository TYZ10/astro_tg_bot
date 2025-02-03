from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation
from .get_info_gpt import main_get_info_gpt
from ...misc import create_aspects


class AnalyzingCompatibilityRelationship(BasicBotOperation):

    text = """Анализ совместимости

Ты выдающийся эксперт в анализе человеческой совместимости. Твоя задача — составить подробный и сбалансированный анализ совместимости двух людей, используя структуру: 1. Введение: объясни важность анализа, метафорически представь их союз и раскрой его суть. 2. Основная энергетика партнёров: опиши их качества, сильные стороны, слабости, роли в отношениях и их влияние друг на друга. 3. Карта совместимости: раскрой, как их особенности взаимодействуют на уровне эмоций, интеллекта, физической и духовной связи; подчеркни как позитивные моменты, так и точки напряжения. 4. Сферы жизни и взаимодействия: проанализируй ключевые аспекты, такие как любовь, семья, доверие, финансы, цели; выдели сильные стороны и потенциальные конфликты. 5. Баланс личностей: объясни, как их качества дополняют или противоречат друг другу, как они проявляют гибкость, стабильность или инициативу. 6. Динамика времени: укажи, как жизненные обстоятельства и изменения могут повлиять на их отношения, выделив ключевые периоды. 7. Глубинные темы: раскрой кармическую природу союза, подсознательные мотивы и темы, которые они привносят в отношения; укажи, что важно видеть для гармонии. 8. Конфликты и точки роста: определи различия и причины напряжений, предложи практические рекомендации для их преодоления и развития через вызовы. 9. Общая миссия: раскрой смысл их союза, чему они учат друг друга, как развиваются вместе и что могут привнести в мир. 10. Заключение: подведи итог, выделяя позитивные и негативные стороны, добавь практические рекомендации и завершай вдохновляющей нотой о гармонии их союза. Не используй астрологические термины, фокусируйся на смысле взаимодействий, психологической и эмоциональной динамике, делая текст сбалансированным с рекомендациями к каждому аспекту.

Данные: {}

{}"""

    async def analyzing_compatibility_relationship(
            self,
            info_partner: list,
            info_user: list,
            message: types.Message,
            state: FSMContext
    ):
        """Анализ совместимости в отношениях"""

        await message.answer("Ожидайте, примерное время 25-35 секунд")

        (place_birth_user, latitude_user, longitude_user, time_birth_user,
         data_birth_user) = info_user
        (place_birth_partner, latitude_partner, longitude_partner,
         time_birth_partner, data_birth_partner) = info_partner

        aspects_user = create_aspects(
            f"{data_birth_user} {time_birth_user}",
            latitude_user,
            longitude_user
        )
        aspects_partner = create_aspects(
            data_birth_partner,
            latitude_partner,
            longitude_partner
        )

        text_gpt = await main_get_info_gpt(
            self.config,
            "",
            self.text.format(aspects_user, aspects_partner)
        )
        (count_generation,
         generation_count_all) = self.operation_db.select_user_info_db(
            f"{self.operation_db.COLUMNS_INFO.generation_count}, "
            f"{self.operation_db.COLUMNS_INFO.generation_count_all}",
            message.from_user.id,
            many=True
        )

        self.operation_db.update_user_info_db(
            {
                self.operation_db.COLUMNS_INFO.generation_count: count_generation - 1,
                self.operation_db.COLUMNS_INFO.generation_count_all: generation_count_all + 1,
            },
            message.from_user.id
        )

        if len(str(text_gpt)) > 4096:
            await message.answer(str(text_gpt)[:4096])
            await message.answer(str(text_gpt)[4096:])
        else:
            await message.answer(
                text=str(text_gpt)
            )

        await message.answer(
            text=f"Количество оставшихся генераций: {count_generation - 1}",
            reply_markup=self.keyboard.main_menu_kb
        )

        await state.clear()

    def create_router(self):
        pass
