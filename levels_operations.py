import sqlite3

def create_table(database, table, rows):
    # ввод в формате: create_table(!имя базы данных!, !имя таблицы!, !список в формате [[название строки, тип данных строчки] * кол-во строчек]!
    # пример: create_table(friends, classmates, [[name, TEXT], [age, INT], [pnone_number, TEXT]]
    con = sqlite3.connect(database)
    table_elements = list()
    for row in rows:
        table_elements.append(' '.join(row))
    cur = con.cursor()
    cur.execute(f"""create table if not exists {table}({', '.join(table_elements)})""")
    con.commit()
    con.close()

def select_from_table(database, table, rows):
    # ввод в формате: create_table(!имя базы данных!, !имя таблицы!, !список в формате [[название строки, значение строки] * кол-во строчек]!
    # пример: create_table(friends, classmates, [[name, TEXT], [age, INT], [pnone_number, TEXT]]
    con = sqlite3.connect(database)
    table_elements = list()
    cur = con.cursor()
    if len(rows) == 1:
        row = rows[0]
        if len(row[0]) == 1:
            result = cur.execute(f"""select {row[0]} from {table}""")
        else:
            result = cur.execute(f"""select {row[0]} from {table} where user_name='{row[1]}'""")
    else: # не доделано
        for row in rows:
            pass
    con.commit()
    con.close()
    return result