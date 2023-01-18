

import psycopg2

from constants import CREATE_MESSAGE_TABLE, CREATE_LIKES_TABLE,  CREATE_TRIGGER, CREATE_TRIGGER_FUNCTION

from utility import trycatch


def getDBConnection(dbname: str):
    conn = psycopg2.connect(
        database=dbname,
        user='postgres',
        password='postgres',
        host='127.0.0.1',
        port='5432'
    )
    conn.autocommit = True
    return conn


def getDBConnectionAndCreateDatabase(dbname: str):
    conn = psycopg2.connect(
        user='postgres',
        password='postgres',
        host='127.0.0.1',
        port='5432'
    )
    conn.autocommit = True

    createDB = f'''CREATE DATABASE {dbname}'''
    cursor = conn.cursor()

    cursor.execute(createDB)
    conn = psycopg2.connect(
        database=dbname,
        user='postgres',
        password='postgres',
        host='127.0.0.1',
        port='5432'
    )
    conn.autocommit = True
    return conn


def init(dbname: str):
    conn = trycatch(getDBConnection, dbname)
    if isinstance(conn, dict):
        conn = trycatch(getDBConnectionAndCreateDatabase, dbname)

    cursor = conn.cursor()
    trycatch(cursor.execute, CREATE_MESSAGE_TABLE)
    trycatch(cursor.execute, CREATE_LIKES_TABLE)
    trycatch(cursor.execute, CREATE_TRIGGER_FUNCTION)
    trycatch(cursor.execute, CREATE_TRIGGER)
    conn.close()
