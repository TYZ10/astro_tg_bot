from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation


class Predictions(BasicBotOperation):

    async def selection_predictions(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ):
        await call.message.answer(
            text="Выберите период предсказания:",
            reply_markup=self.keyboard.selection_predictions_ikb
        )

    async def get_predictions(
            self,
            call: types.CallbackQuery,
            state: FSMContext):
        _, period = call.data.split("_", maxsplit=1)

        if period == "day":
            pass
        elif period == "month":
            pass
        elif period == "year":
            pass

    async def create_router(self):
        self.router.callback_query(
            self.selection_predictions,
            F.data == "start generation",
            StateFilter(AllTypesGeneration.predictions.state)
        )
        self.router.callback_query(
            self.get_predictions,
            F.data.split("_")[0] == "select prediction",
            StateFilter(AllTypesGeneration.predictions.state)
        )
