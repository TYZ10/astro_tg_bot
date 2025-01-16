from psycopg2 import _psycopg

from . import COLUMNS_INFO


def insert_new_user(cur: _psycopg.cursor, conn: _psycopg.connection,
                    name_db: str, userid: str, full_name: str, username: str,
                    **kwargs) -> bool:
    """Добавление нового пользователя в БД, если новый вернёт True"""
    cur.execute(f'SELECT * FROM "{name_db}" WHERE userid = %s',
                (userid,))

    if cur.fetchone() is None:
        cur.execute(f'INSERT INTO "{name_db}" '
                    f'({COLUMNS_INFO.userid}, {COLUMNS_INFO.full_name},'
                    f'{COLUMNS_INFO.username})'
                    f'VALUES(%s, %s ,%s)',
                    (userid, full_name, username))
        conn.commit()
        return True
    return False
