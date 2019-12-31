import mysql.connector

def connection(db):
    conn = mysql.connector.connect(user='root', password='shornabho',
                              host='localhost',
                              database=db)
    c = conn.cursor()

    return c, conn