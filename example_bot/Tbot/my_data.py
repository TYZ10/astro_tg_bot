import logging
from datetime import datetime

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import (
    BasicBotOperation, states, AnalyzingCompatibilityRelationship,
    AllTypesGeneration
)


class MyDataBot(BasicBotOperation):

    def __init__(self, analyz_rel: AnalyzingCompatibilityRelationship):
        super().__init__(
            analyz_rel.config,
            analyz_rel.operation_db,
            analyz_rel.keyboard
        )
        self.analyz_rel: AnalyzingCompatibilityRelationship = analyz_rel

    async def my_data_handler(self, message: types.Message):
        col_info = self.operation_db.COLUMNS_INFO

        data_birth, time_birth, place_birth = self.operation_db.select_user_info_db(
            f"{col_info.data_birth}, {col_info.time_birth}, "
            f"{col_info.place_birth}",
            message.from_user.id,
            many=True
        )

        if not (data_birth and time_birth and place_birth):
            data_birth = "Отсутствует"
            time_birth = "Отсутствует"
            place_birth = "Отсутствует"

        await message.answer(
            text=f"Пользователь: {message.from_user.full_name}\n"
                 f"ID: <code>{message.from_user.id}</code>\n\n"
                 f"Дата рождения: {data_birth}\n"
                 f"Время рождения: {time_birth}\n"
                 f"Место рождения: {place_birth}\n",
            reply_markup=self.keyboard.my_data_ikb,
            parse_mode="HTML"
        )

    async def modify_my_data(self,
                             call: types.CallbackQuery,
                             state: FSMContext):
        current_state = await state.get_state()

        if current_state == "states:analyzing_compatibility_relationship":
            is_partner = True
        else:
            is_partner = False

        await state.set_state(states.data_birth)
        await state.update_data(is_partner=is_partner)

        if is_partner:
            text = ("Введите дату рождения партнёра в "
            "формате YYYY MM DD.\n\n"
            "Пример: 2000 01 21")
        else:
            text = ("Введите дату вашего рождения в "
            "формате YYYY MM DD.\n\n"
            "Пример: 2000 01 21")

        await call.message.answer(text=text,
                                  reply_markup=self.keyboard.abolition_ikb)

    async def get_data_birth(self, message: types.Message, state: FSMContext):
        data_birth = message.text
        try:
            data_birth = datetime.strptime(data_birth, '%Y %m %d')
        except:
            await message.answer(
                text=("Введён неверный формат даты."
                     "Введите дату рождения в "
                     "формате YYYY MM DD (год месяц день) числами!\n\n"
                     "Пример: 2000 01 21"),
                reply_markup=self.keyboard.abolition_ikb)
            return

        await message.answer(
            text="Введите время рождения в формате HH MM SS.\n\n",
            reply_markup=self.keyboard.abolition_ikb
        )
        await state.set_state(states.time_birth)
        await state.update_data(data_birth=data_birth)

    async def get_time_birth(self, message: types.Message, state: FSMContext):
        time_birth = message.text
        try:
            time_birth = datetime.strptime(time_birth, '%H %M %S').time()
        except:
            await message.answer(
                text=("Введён неверный формат времени."
                     "Введите время рождения в "
                     "формате HH MM SS (Часы минуты секунды) числами!\n\n"
                     "Пример: 12 30 02"),
                reply_markup=self.keyboard.abolition_ikb)
            return
        await message.answer(
            text="Введите место рождения.",
            reply_markup=self.keyboard.abolition_ikb
        )
        await state.set_state(states.place_birth)
        await state.update_data(time_birth=time_birth)

    async def get_place_birth(self,
                              message: types.Message,
                              state: FSMContext):
        await message.answer(text="Обрабатываю информацию, подождите...")
        st = await state.get_data()
        place_birth = message.text
        data_birth = st['data_birth']
        time_birth = st['time_birth']
        is_partner = st['is_partner']

        result = self.config.geocoder.geocode(
            place_birth,
            language='ru'
        )
        try:
            latitude = result['results'][0]['geometry']['lat'] # Широта
            longitude = result['results'][0]['geometry']['lng'] # Долгота
        except:
            try:
                latitude = result[0]['geometry']['lat']  # Широта
                longitude = result[0]['geometry']['lng']  # Долгота
            except:
                await message.answer(
                    text="Введите место рождения точнее.",
                    reply_markup=self.keyboard.abolition_ikb)
                return

        await state.clear()

        if is_partner:
            col_info = self.operation_db.COLUMNS_INFO

            (place_birth_2, latitude_2, longitude_2, time_birth_2,
             data_birth_2) = self.operation_db.select_user_info_db(
                f"{col_info.place_birth},"
                f"{col_info.latitude},"
                f"{col_info.longitude},"
                f"{col_info.time_birth},"
                f"{col_info.data_birth}",
                message.from_user.id,
                many=True
            )

            await self.analyz_rel.analyzing_compatibility_relationship(
                [place_birth, latitude, longitude, time_birth, data_birth],
                [place_birth_2, latitude_2, longitude_2,
                 time_birth_2, data_birth_2],
                message,
                state
            )
        else:
            col_info = self.operation_db.COLUMNS_INFO

            self.operation_db.update_user_info_db(
                {
                    col_info.place_birth: place_birth,
                    col_info.latitude: latitude,
                    col_info.longitude: longitude,
                    col_info.time_birth: time_birth,
                    col_info.data_birth: data_birth,
                },
                userid=message.from_user.id
            )

            await message.answer(text="Данные успешно сохранены.",
                                 reply_markup=self.keyboard.main_menu_kb)

    def create_router(self):
        self.router.message.register(self.my_data_handler, F.text == "Мои данные")
        self.router.callback_query.register(self.modify_my_data,
                                   F.data == "modify my data")
        self.router.message.register(self.get_data_birth,
                            StateFilter(states.data_birth))
        self.router.message.register(self.get_time_birth,
                            StateFilter(states.time_birth))
        self.router.message.register(self.get_place_birth,
                            StateFilter(states.place_birth))
        self.router.callback_query.register(
            self.modify_my_data,
            F.data == "start generation",
            StateFilter(
                AllTypesGeneration.analyzing_compatibility_relationship.state
            )
        )
