from psycopg2 import connect, _psycopg

from .init_db import init_db
from .insert_db import insert_new_user
from .select_db import select_user_info_db, select_all_user_info_db
from .update_db import update_user_info_db, update_all_user_info_db
from .delete_db import delete_db


class OperationDataBaseBot:
    def __init__(self, name_db: str, ps_user: str,
                 ps_password: str, ps_dbname: str,
                 is_delete_db: bool = False):
        from . import ColumnsInfoDB, COLUMNS_INFO

        self.name_db: str = name_db
        self.COLUMNS_INFO: ColumnsInfoDB = COLUMNS_INFO

        self.conn: _psycopg.connection = connect(
            user=ps_user,
            password=ps_password,
            dbname=ps_dbname
        )

        self.cur: _psycopg.cursor = self.conn.cursor()

        if is_delete_db:
            self.__delete_db()

        self.__operation_db(init_db)

    def __operation_db(self, operation_func, *args, **kwargs):

        result = operation_func(*args, cur=self.cur, conn=self.conn,
                                name_db=self.name_db,
                                **kwargs)
        return result

    def insert_new_user(self, userid, full_name, username) -> bool:
        return self.__operation_db(
            insert_new_user,
            userid=userid,
            full_name=full_name,
            username=username
        )

    def select_user_info_db(self, column, info_value,
                            value="userid", many=False):
        self.__operation_db(
            select_user_info_db,
            column=column,
            info_value=info_value,
            value=value,
            many=many,
        )

    def select_all_user_info_db(self, column):
        self.__operation_db(
            select_all_user_info_db,
            column=column,
        )

    def update_user_info_db(self, dict_info: dict, userid: int):
        self.__operation_db(
            update_user_info_db,
            dict_info=dict_info,
            userid=userid,
        )

    def update_all_user_info_db(self, dict_info: dict):
        self.__operation_db(
            update_all_user_info_db,
            dict_info=dict_info,
        )

    def __delete_db(self):
        """НЕ РЕКОМЕНДУЕТСЯ ИСПОЛЬЗОВАТЬ ТАК КАК УДАЛЯЕТ ВСЮ ТАБЛИЦУ!!"""
        self.__operation_db(
            delete_db
        )
