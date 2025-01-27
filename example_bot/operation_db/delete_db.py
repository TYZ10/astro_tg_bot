from psycopg2 import _psycopg


def delete_db(cur: _psycopg.cursor, conn: _psycopg.connection,
            name_db: str, **kwargs):
    """Удаление БД"""
    cur.execute(f'DROP TABLE "{name_db}"')
    conn.commit()
