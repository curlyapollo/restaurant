from mysql import connector
from mysqlx import errorcode

# select request to database
def select_from_db(query: str) -> list:
    try:
        cnx = connector.connect(user='root',
                                password='1234',
                                host="localhost",
                                port=3306,
                                database='cooker')
    except connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()
        cnx.reconnect()
        cursor = cnx.cursor()
        cursor.execute(query)
        return cursor.fetchall()


# insert or update request to database
def insert_to_db(query: str) -> None:
    try:
        cnx = connector.connect(user='root',
                                password='1234',
                                host="localhost",
                                port=3306,
                                database='cooker')
    except connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()
        cnx.reconnect()
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
