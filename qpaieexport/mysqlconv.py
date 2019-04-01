import mysql.connector


def create_table_sqlgen(table_name, column_list):
    """
    Generate the SQL syntax to create the table
    table_name: table name string
    column_list: tables values (each row is a list)
    """
    columns = []

    for item in column_list:
        if item[1] == type(1) or item[1] == "integer":  # integer
            datatype = "INT"
        elif item[1] == type(True) or item[1] == "boolean":  # boolean
            datatype = "INT"
        elif item[1] == type(1.0) or item[1] == "float":  # float
            datatype = "FLOAT"
        elif item[1] == type("A") or item[1] == "text":  # text
            datatype = "VARCHAR(100)"
        elif item[1] == type(datetime.now()) or item[1] == "date":
            datatype = "DATETIME"
        else:
            datatype = "VARCHAR(100)"

        columns.append(item[0] + " " + datatype)

    return "CREATE TABLE {} ({})".format(table_name, ", ".join(columns))


def fill_table_sqlgen(table_name, column_list):

    columns = []
    for item in column_list:
        columns.append(item)
    sql = """
    INSERT INTO {} (
        {})
    VALUES (
        {}
    )
    """.format(
        table_name, ", ".join(columns), ", ".join(["%s"] * len(column_list))
    )
    return sql


class connect_msyql(object):
    def __init__(self, params):

        self.params = params

    def connect(self):

        try:
            self.conn = mysql.connector.connect(**self.params)
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return False
        if self.conn.is_connected():
            print("MySQL connected")

    def disconnect(self):

        print("I'm out")
        self.conn.commit()
        self.conn.close()

    def create_table(self, table_name, column_list):

        self.cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))

        sql = create_table_sqlgen(table_name, column_list)
        print(sql)
        self.cursor.execute(sql)

    def fill_table(self, table_name, column_list, row_list):

        sql = fill_table_sqlgen(table_name, column_list)
        print(sql)

        self.cursor.executemany(sql, row_list)


if __name__ == "__main__":
    from datetime import datetime

    params = {
        "host": "10.0.0.117",
        "user": "root",
        "passwd": "rangit9562",
        "database": "paie_odenval",
    }

    db = connect_msyql(params)
    db.connect()

    # data = (
    #     ("matricule", type(1), None, 10, 10, 0, True),
    #     ("nom", type("A"), None, 50, 50, 0, True),
    #     ("zedate", type(datetime(2000, 8, 2)), None, 53, 53, 0, True)
    # )

    # db.create_table("salaries", data)

    # fill_data = [
    #     ["45", "CONDE FOUSSENI", datetime(2018, 7, 2, 0, 0)],
    #     ["46", "CHENIN SAMUEL", datetime(2018, 7, 9, 0, 0)],
    #     ["47", "BUFFARD LISE", datetime(2018, 8, 27, 0, 0)],
    # ]

    # # print(fill_table_sqlgen("salaries", ["matricule", "nom", "zedate"]))

    # db.fill_table("salaries", ["matricule", "nom", "zedate"], fill_data)

    from qpaietools import QueryPaie

    o = QueryPaie()
    o.connect("C:/Users/nicolas/Documents/Pydio/Sources/odenval_qpaie.mdb")
    # db = connect_msyql()

    data, columns = o.employes()
    db.create_table("Employes", columns)
    heads = [x[0] for x in columns]
    print(heads)
    db.fill_table("Employes", heads, data)

    data, columns = o.bulletins()
    db.create_table("Bulletins", columns)
    heads = [x[0] for x in columns]
    print(heads)
    db.fill_table("Bulletins", heads, data)

    db.disconnect()

    # db.fill_table("Employes", columns, data)

    # data, columns = o.bulletins()
    # db.create_table("Bulletins", columns)
    # db.fill_table("Bulletins", columns, data)

    # o.disconnect()
