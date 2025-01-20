from aiogram.fsm.state import State
from aiogram.filters import BaseFilter
from aiogram.types import Message


class TypeGeneration:
    def __init__(self, text: str, state: State):
        self.text: str = text
        self.state: State = state


class AllTypesGeneration(BaseFilter):
    from example_bot.Tbot import states

    natal_chart_analysis: TypeGeneration = TypeGeneration(
        "Анализ натальной карты",
        states.natal_chart_analysis
    )
    predictions: TypeGeneration = TypeGeneration(
        "Прогнозы",
        states.predictions
    )
    horoscope_for_business: TypeGeneration = TypeGeneration(
        "Гороскоп для бизнеса",
        states.horoscope_for_business
    )
    recommendations_self_actualization: TypeGeneration = TypeGeneration(
        "Рекомендации по самореализации",
        states.recommendations_self_actualization
    )
    analyzing_compatibility_relationship: TypeGeneration = TypeGeneration(
        "Анализ совместимости в отношениях",
        states.analyzing_compatibility_relationship
    )
    astrological_forecast_health: TypeGeneration = TypeGeneration(
        "Астрологический прогноз для здоровья",
        states.astrological_forecast_health
    )

    def __call__(self, message: Message) -> bool:
        text = message.text

        if (
                text == self.natal_chart_analysis.text or
                text == self.predictions.text or
                text == self.horoscope_for_business.text or
                text == self.recommendations_self_actualization.text or
                text == self.analyzing_compatibility_relationship.text or
                text == self.astrological_forecast_health.text
        ):
            return True
        return False
