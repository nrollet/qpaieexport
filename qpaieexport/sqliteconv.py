import sqlite3


def create_table_sqlgen(table_name, column_list):
    """
    Generate the SQL syntax to create the table
    """
    columns = []

    for item in column_list:
        if item[1] == type(1) or item[1] == "integer":  # integer
            datatype = "integer"
        elif item[1] == type(True) or item[1] == "boolean":  # boolean
            datatype = "integer"
        elif item[1] == type(1.0) or item[1] == "float":  # float
            datatype = "real"
        elif item[1] == type("A") or item[1] == "text":  # text
            datatype = "text"
        else:
            datatype = "text"

        columns.append(item[0] + " " + datatype)

    return "CREATE TABLE {} ({})".format(table_name, ", ".join(columns))


def fill_table_sqlgen(table_name, column_list):

    columns = []
    for item in column_list:
        columns.append(item[0])
    sql = """
    INSERT INTO {} (
        {})
    VALUES (
        {}
    )
    """.format(
        table_name, ", ".join(columns), ", ".join(["?"] * len(column_list))
    )
    return sql


# c.execute(
#     """
#     INSERT INTO {} (
#         inbox,
#         date,
#         exped,
#         exped_nom,
#         dest,
#         copi,
#         objet
#     ) VALUES (%s, %s, %s, %s, %s, %s, %s)
#     """.format(table),


class setup_db(object):
    def __init__(self, filename):

        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

    def close(self):

        self.conn.commit()
        self.conn.close()

    def create_table(self, table_name, column_list):

        self.cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))

        sql = create_table_sqlgen(table_name, column_list)
        self.cursor.execute(sql)

    def fill_table(self, table_name, column_list, row_list):

        sql = fill_table_sqlgen(table_name, column_list)
        print(sql)

        self.cursor.executemany(sql, row_list)


if __name__ == "__main__":
    import datetime

    # data = (
    #     ("CodeEtablissement", type(1), None, 10, 10, 0, True),
    #     ("Libelle", type("A"), None, 50, 50, 0, True),
    #     ("SmicH35", type(1.0), None, 53, 53, 0, True),
    # )

    # fill_data = [
    #     ["45", "CONDE FOUSSENI", datetime.datetime(2018, 7, 2, 0, 0), None],
    #     ["46", "CHENIN SAMUEL", datetime.datetime(2018, 7, 9, 0, 0), None],
    #     ["47", "BUFFARD LISE", datetime.datetime(2018, 8, 27, 0, 0), None],
    # ]

    # fill_table_sqlgen("prout", data)

    from qpaietools import QueryPaie

    o = QueryPaie()
    o.connect("C:/Users/nicolas/Documents/Pydio/Sources/odenval_qpaie.mdb")
    db = setup_db("sqlite.db")

    data, columns = o.employes()
    db.create_table("Employes", columns)
    db.fill_table("Employes", columns, data)

    data, columns = o.bulletins()
    db.create_table("Bulletins", columns)
    db.fill_table("Bulletins", columns, data)

    o.disconnect()
    db.close()
