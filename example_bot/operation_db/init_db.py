from psycopg2 import _psycopg

from . import COLUMNS_INFO


def init_db(cur: _psycopg.cursor, conn: _psycopg.connection,
            name_db: str, **kwargs):

    cur.execute(f'''CREATE TABLE IF NOT EXISTS "{name_db}"(
        {COLUMNS_INFO.userid} BIGINT PRIMARY KEY,
        {COLUMNS_INFO.username} VARCHAR(32),
        {COLUMNS_INFO.full_name} VARCHAR(128),
        {COLUMNS_INFO.first_arrival} TIMESTAMP DEFAULT NOW(),
        {COLUMNS_INFO.last_action} TIMESTAMP DEFAULT NOW(),
        {COLUMNS_INFO.generation_count} SMALLINT DEFAULT 0,
        {COLUMNS_INFO.payments_start} SMALLINT DEFAULT 4,
        {COLUMNS_INFO.data_birth} DATE DEFAULT NULL,
        {COLUMNS_INFO.time_birth} TIME DEFAULT NULL,
        {COLUMNS_INFO.place_birth} VARCHAR(200) DEFAULT NULL,
        {COLUMNS_INFO.latitude} FLOAT DEFAULT NULL,
        {COLUMNS_INFO.longitude} FLOAT DEFAULT NULL,
        {COLUMNS_INFO.referrals_count} INTEGER DEFAULT 0,
        {COLUMNS_INFO.referral_user} BIGINT DEFAULT NULL
    )''')
    conn.commit()
