import pymysql.cursors
import os

def get_conn():
    db_host = os.getenv("DB_IP", "172.17.0.1")
    # localhost = '127.0.0.1'
    db_port = os.getenv("DB_PORT", "53306")
    conn = pymysql.connect( host = db_host, 
                            port = int(db_port),
                            user = 'mnist', 
                            password = '1234',
                            database = 'mnistdb',
                            cursorclass = pymysql.cursors.DictCursor)
    return conn

# db connection이후 data select
def select(query: str, size = -1):
    conn = get_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchmany(size)

    return result

# db connection이후 
def dml(sql, *values):
    conn = get_conn()

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount
