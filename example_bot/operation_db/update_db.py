def update_user_info_db(dict_info: dict, userid, name_db: str,
                        cur, conn, **kwargs):
    from . import COLUMNS_INFO

    sql = f'UPDATE "{name_db}" SET '

    info = dict_info.items()

    if len(info) > 0:
        for column, value in info:
            sql += f'{column} = %s, '

        sql = sql[:-2] + f' WHERE {COLUMNS_INFO.userid} = {userid}'

        cur.execute(sql, tuple(dict_info.values()))
        conn.commit()


def update_all_user_info_db(dict_info: dict, name_db: str, cur, conn,
                            **kwargs):
    sql = f'UPDATE "{name_db}" SET '

    info = dict_info.items()

    if len(info) > 0:
        for column, value in info:
            sql += f'{column} = %s, '

        sql = sql[:-2]

        cur.execute(sql, tuple(dict_info.values()))
        conn.commit()
