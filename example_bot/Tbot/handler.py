from .help import HelpBot
from .main_menu import MainMenuBot
from .my_data import MyDataBot
from .payments import PaymentsBot
from .ref_system import RefSystemBot
from .start import StartBot
from .generation.analyzing_compatibility_relationship import (
    AnalyzingCompatibilityRelationship)
from .generation.analyzing_personal_strengths import AnalyzingPersonalStrengths
from .generation.astrological_forecast_health import AstrologicalForecastHealth
from .generation.horoscope_for_business import HoroscopeForBusiness
from .generation.natal_chart_analysis import NatalChartAnalysis
from .generation.predictions import Predictions
from .generation.recommendations_actualization import (
    RecommendationsActualization)
from .generation.set_time_prediction import SetPredictions
from .generation.start_generation import StartAllGeneration
from . import (
    OperationDataBaseBot, ConfigBot
)
from .apsheduler import ApshedulerBot


class InitHandlerBot:
    def __init__(
            self,
            config: ConfigBot,
            operation_db: OperationDataBaseBot,
            keyboard
    ):
        from . import KeyboardBot

        self.config: ConfigBot = config
        self.operation_db: OperationDataBaseBot = operation_db
        self.keyboard: KeyboardBot = keyboard

        self.help = HelpBot(config, operation_db, keyboard)
        self.main_menu = MainMenuBot(config, operation_db, keyboard)
        self.payments = PaymentsBot(config, operation_db, keyboard)
        self.ref_system = RefSystemBot(config, operation_db, keyboard)
        self.start = StartBot(config, operation_db, keyboard)
        self.analyzing_compatibility_relationship = (
            AnalyzingCompatibilityRelationship(config, operation_db, keyboard)
        )
        self.my_data = MyDataBot(self.analyzing_compatibility_relationship)
        self.analyzing_personal_strengths = AnalyzingPersonalStrengths(
            config, operation_db, keyboard
        )
        self.astrological_forecast_health = AstrologicalForecastHealth(
            config, operation_db, keyboard
        )
        self.horoscope_for_business = HoroscopeForBusiness(
            config, operation_db, keyboard
        )
        self.natal_chart_analysis = NatalChartAnalysis(
            config, operation_db, keyboard
        )
        self.predictions = Predictions(config, operation_db, keyboard)
        self.recommendations_actualization = RecommendationsActualization(
            config, operation_db, keyboard
        )
        self.start_all_generation = StartAllGeneration(
            config, operation_db, keyboard
        )
        self.apscheduler = ApshedulerBot(config, operation_db, keyboard)
        self.set_time_prediction = SetPredictions(
            config, operation_db, keyboard, self.apscheduler
        )

        self.__register_all_handlers()

    def __register_all_handlers(self):
        self.config.dp.startup.register(self.apscheduler.on_startup)

        self.config.dp.include_routers(
            self.start.router,
            self.help.router,
            self.main_menu.router,
            self.payments.router,
            self.ref_system.router,
            self.analyzing_compatibility_relationship.router,
            self.my_data.router,
            self.analyzing_personal_strengths.router,
            self.astrological_forecast_health.router,
            self.horoscope_for_business.router,
            self.natal_chart_analysis.router,
            self.predictions.router,
            self.recommendations_actualization.router,
            self.start_all_generation.router,
            self.set_time_prediction.router
        )
