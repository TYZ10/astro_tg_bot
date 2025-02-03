from aiogram.fsm.state import State
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class TypeGeneration:
    def __init__(self, text: str, state: State):
        self.text: str = text
        self.state: State = state


class AllTypesGeneration(BaseFilter):
    from example_bot.Tbot import states

    natal_chart_analysis: TypeGeneration = TypeGeneration(
        "🪐 Анализ натальной карты",
        states.natal_chart_analysis
    )
    predictions: TypeGeneration = TypeGeneration(
        "select prediction",
        states.predictions
    )
    horoscope_for_business: TypeGeneration = TypeGeneration(
        "💼 Бизнес-гороскоп",
        states.horoscope_for_business
    )
    recommendations_self_actualization: TypeGeneration = TypeGeneration(
        "🚀 Рекомендации по самореализации",
        states.recommendations_self_actualization
    )
    analyzing_compatibility_relationship: TypeGeneration = TypeGeneration(
        "💞 Анализ совместимости в отношениях",
        states.analyzing_compatibility_relationship
    )
    astrological_forecast_health: TypeGeneration = TypeGeneration(
        "Прогноз для здоровья",
        states.astrological_forecast_health
    )
    analyzing_personal_strengths: TypeGeneration = TypeGeneration(
        "✨ Анализ сильных сторон личности",
        states.analyzing_personal_strengths
    )

    def __init__(self):
        self.types = {
            "🪐 Анализ натальной карты": self.natal_chart_analysis.state,
            "select prediction": self.predictions.state,
            "💼 Бизнес-гороскоп": self.horoscope_for_business.state,
            "🚀 Рекомендации по самореализации":
                self.recommendations_self_actualization.state,
            "💞 Анализ совместимости в отношениях":
                self.analyzing_compatibility_relationship.state,
            "Прогноз для здоровья":
                self.astrological_forecast_health.state,
            "✨ Анализ сильных сторон личности":
                self.analyzing_personal_strengths.state,
        }

    def __getitem__(self, item):
        return self.types[item.split("_")[0]]

    async def __call__(self, message: Message or CallbackQuery) -> bool:
        if isinstance(message, Message):
            text = message.text

            if (
                    text == self.natal_chart_analysis.text or
                    text == self.horoscope_for_business.text or
                    text == self.recommendations_self_actualization.text or
                    text == self.analyzing_compatibility_relationship.text or
                    text == self.astrological_forecast_health.text or
                    text == self.analyzing_personal_strengths.text
            ):
                return True
            return False
        else:
            text = message.data

            if (
                    text == self.natal_chart_analysis.text or
                    text.split("_")[0] == self.predictions.text or
                    text == self.horoscope_for_business.text or
                    text == self.recommendations_self_actualization.text or
                    text == self.analyzing_compatibility_relationship.text or
                    text == self.astrological_forecast_health.text or
                    text == self.analyzing_personal_strengths.text
            ):
                return True
            return False
