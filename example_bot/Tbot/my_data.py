from datetime import datetime

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import BasicBotOperation, states


class MyDataBot(BasicBotOperation):
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
            reply_markup=self.keyboard.my_data_ikb
        )

    async def modify_my_data(self,
                             call: types.CallbackQuery,
                             state: FSMContext):
        await state.set_state(states.data_birth)

        await call.message.answer(text="Введите дату вашего рождения в "
                                       "формате YYYY MM DD.\n\n"
                                       "Пример: 2000 01 21",
                                  reply_markup=self.keyboard.abolition_ikb)

    async def get_data_birth(self, message: types.Message, state: FSMContext):
        data_birth = message.text
        try:
            data_birth = datetime.strptime(data_birth, '%Y %m %d')
        except:
            await message.answer(
                text="Введён неверный формат даты."
                     "Введите дату вашего рождения в "
                     "формате YYYY MM DD (год месяц день) числами!\n\n"
                     "Пример: 2000 01 21",
                reply_markup=self.keyboard.abolition_ikb)
            return

        await message.answer(
            text="Введите время вашего рождения в формате HH MM SS.\n\n",
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
                text="Введён неверный формат времени."
                     "Введите время вашего рождения в "
                     "формате HH MM SS (Часы минуты секунды) числами!\n\n"
                     "Пример: 12 30 02",
                reply_markup=self.keyboard.abolition_ikb)
            return
        await message.answer(
            text="Введите место вашего рождения.",
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

        result = await self.config.geocoder.geocode_async(
            place_birth,
            language='ru'
        )
        try:
            latitude = result['results'][0]['geometry']['lat'] # Широта
            longitude = result['results'][0]['geometry']['lng'] # Долгота
        except:
            await message.answer(
                text="Введите место вашего рождения точнее.",
                reply_markup=self.keyboard.aboцlition_ikb)
            return

        await state.clear()

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

    async def create_router(self):
        self.router.message(self.my_data_handler, F.text == "Мои данные")
        self.router.callback_query(self.modify_my_data,
                                   F.text == "modify my data")
        self.router.message(self.get_data_birth,
                            StateFilter(states.data_birth))
        self.router.message(self.get_time_birth,
                            StateFilter(states.time_birth))
        self.router.message(self.get_place_birth,
                            StateFilter(states.place_birth))


