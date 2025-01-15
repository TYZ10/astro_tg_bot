from psycopg2 import _psycopg


def init_db(cur: _psycopg.cursor, conn: _psycopg.connection,
            name_db: str, **kwargs):

    cur.execute(f'''CREATE TABLE IF NOT EXISTS "{name_db}"(
    )''')
