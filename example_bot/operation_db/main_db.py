from psycopg2 import connect, _psycopg

from .init_db import init_db
from .insert_db import insert_new_user
from example_bot.Config_bot import ConfigBot


class OperationDataBaseBot:
    def __init__(self, name_db: str, COLUMNS_INFO, config: ConfigBot):
        from .columns_info import ColumnsInfoDB

        self.name_db: str = name_db
        self.COLUMNS_INFO: ColumnsInfoDB = COLUMNS_INFO

        self.conn: _psycopg.connection = connect(
            user=config.POSTGRESQL_USER,
            password=config.POSTGRESQL_PASSWORD,
            dbname=config.POSTGRESQL_DBNAME
        )
        self.cur: _psycopg.cursor = self.conn.cursor()

        self.__operation_db(init_db)

    def __operation_db(self, operation_func, *args, **kwargs):

        result = operation_func(*args, cur=self.cur, conn=self.conn,
                                name_db=self.name_db,
                                **kwargs)
        return result

    def insert_new_user(self, userid, full_name, username):
        self.__operation_db(
            insert_new_user,
            userid=userid,
            full_name=full_name,
            username=username
        )
