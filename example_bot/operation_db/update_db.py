from . import COLUMNS_INFO


def update_user_info_db(dict_info: dict, userid, name_db: str,
                        cur, conn, **kwargs):
    sql = f'UPDATE "{name_db}" SET '

    info = dict_info.items()

    if len(info) > 0:
        for column, value in dict_info.items():
            sql += f'{column} = %s AND'

        sql = sql[:-3] + f' WHERE {COLUMNS_INFO.userid} = {userid}'

        cur.execute(sql, dict_info.values())
        conn.commit()
