from psycopg2 import _psycopg
from datetime import datetime

from . import COLUMNS_INFO

def insert_new_user(cur: _psycopg.cursor, conn: _psycopg.connection,
            name_db: str, **kwargs):
    cur.execute(f'INSERT INTO "{name_db}" '
                f'({COLUMNS_INFO.userid})'
                f'VALUES(%s, %s ,%s, %s, %s, %s, %s, %s)',
                ())
    conn.commit()