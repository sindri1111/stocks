import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def execute_sql(conn, sql_command, commit=False):
    """ Executes SQL statement """
    try:
        c = conn.cursor()
        c.execute(sql_command)
        if commit:
            conn.commit()

        return c
    except Error as e:
        print(e)

def create_table_command(tablename, headers, types):
    """Creates the string command for creating a table in SQL"""
    return """CREATE TABLE IF NOT EXISTS {tablename} (
    id integer PRIMARY KEY,
    {rest})
    """.format(
        tablename=tablename,
        rest=",\n".join([headers[i]+" "+types[i] for i in range(len(headers))])
    )

def insert_into_command(tablename, headers, values):
    """Inserts values into table"""
    if not isinstance(values, zip):
        return """INSERT INTO {tablename} ({headers})
        VALUES ({values})
        """.format(tablename=tablename, headers='"'+'","'.join(headers)+'"', values=",".join([str(i) for i in values]))
    elif isinstance(values, zip):
        values = list(values)
        vals = ",\n".join(["("+",".join([str(i) for i in values[j]])+")" for j in range(len(values))])
        return """INSERT INTO {tablename} ({headers})
        VALUES {values}
        """.format(tablename=tablename, headers='"'+'","'.join(headers)+'"', values=vals)

def get_table_names(conn):
    return [i[0] for i in execute_sql(conn, "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

def empty_table(tablename, conn=None, db_path=None):
    close_on_end = False
    empty = False
    if conn is None:
        conn = create_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM "{}" """.format(tablename))
        ret = c.fetchall()
        if len(ret) == 0:
            empty = True
        if close_on_end:
            conn.close()
    except sqlite3.OperationalError:
        empty = True
    return empty


#conn = create_connection("test.db")
##execute_sql(conn, create_table_command("Test", ["hi", "my", "name", "iiss"], ["text", "int", "float", "int"]))
#print(insert_into_command("Test", ["hi", "my", "name", "iiss"], ["'hallo'", 3, 2.43, 45,"'hallo'", 3, 2.43, 45,"'hallo'", 3, 2.43, 45,"'hallo'", 3, 2.43, 45,"'hallo'", 3, 2.43, 45,"'hallo'", 3, 2.43, 45]))
#execute_sql(conn, insert_into_command("Test", ["hi", "my", "name", "iiss"], ["'hallo'", 3, 2.43, 45,"'hallo'", 3, 2.43, 45,"'hallo'", 3, 2.43, 45,"'hallo'", 3, 2.43, 45,"'hallo'", 3, 2.43, 45,"'hallo'", 3, 2.43, 45]))
#conn.commit()