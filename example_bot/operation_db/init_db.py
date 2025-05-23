from psycopg2 import _psycopg


def init_db(cur: _psycopg.cursor, conn: _psycopg.connection,
            name_db: str, **kwargs):
    from . import COLUMNS_INFO

    cur.execute(f'''CREATE TABLE IF NOT EXISTS "{name_db}"(
        {COLUMNS_INFO.userid} BIGINT PRIMARY KEY,
        {COLUMNS_INFO.username} VARCHAR(32),
        {COLUMNS_INFO.full_name} VARCHAR(128),
        {COLUMNS_INFO.first_arrival} TIMESTAMP DEFAULT NOW(),
        {COLUMNS_INFO.last_action} TIMESTAMP DEFAULT NOW(),
        {COLUMNS_INFO.generation_count} SMALLINT DEFAULT 4,
        {COLUMNS_INFO.payments_end} TIMESTAMP DEFAULT NULL,
        {COLUMNS_INFO.data_birth} DATE DEFAULT NULL,
        {COLUMNS_INFO.time_birth} TIME DEFAULT NULL,
        {COLUMNS_INFO.place_birth} VARCHAR(200) DEFAULT NULL,
        {COLUMNS_INFO.latitude} FLOAT DEFAULT NULL,
        {COLUMNS_INFO.longitude} FLOAT DEFAULT NULL,
        {COLUMNS_INFO.referrals_count} INTEGER DEFAULT 0,
        {COLUMNS_INFO.referral_user} BIGINT DEFAULT NULL,
        {COLUMNS_INFO.generation_count_all} INTEGER DEFAULT 0,
        {COLUMNS_INFO.payments_id} VARCHAR(100) DEFAULT NULL,
        {COLUMNS_INFO.referral_all_count_user} INTEGER DEFAULT 0,
        {COLUMNS_INFO.referral_all_count_points_user} INTEGER DEFAULT 0,
        {COLUMNS_INFO.time_prediction} TIME DEFAULT NULL,
        {COLUMNS_INFO.aspects} TEXT DEFAULT NULL
    )''')

    cur.execute(
        f"SELECT column_name FROM information_schema.columns WHERE "
        f"table_name='{name_db}' AND column_name='{COLUMNS_INFO.aspects}'")
    if cur.fetchone() is None:
        # Если колонки нет, добавим ее
        cur.execute(
            f'ALTER TABLE {name_db} ADD COLUMN '
            f'{COLUMNS_INFO.aspects} TEXT DEFAULT NULL;')

    conn.commit()
