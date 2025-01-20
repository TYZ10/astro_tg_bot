from aiogram.fsm.state import State


class TypeGeneration:
    def __init__(self, text: str, state: State):
        self.text: str = text
        self.state: State = state


class AllTypesGeneration:
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
