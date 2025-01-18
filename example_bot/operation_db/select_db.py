from . import COLUMNS_INFO


def select_user_info_db(column, info_value,
                        value, many, name_db: str, cur, **kwargs):
    cur.execute(f'SELECT {column} FROM "{name_db}" WHERE {value} = %s',
                (info_value,))
    result = cur.fetchone()

    if many:
        return result

    try:
        return result[0]
    except:
        return result