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
    except Error as e:
        print("\n\n\n"+e+"\n\n\n")

    return conn

def create_img(conn, img):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    try:
        sql = ''' INSERT INTO IMG_URLS(ID,URL)
                  VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, img)
        cur.close()
        return cur.lastrowid
    except Error as e:
        print("\n\n\n"+e+"\n\n\n")

def select_img(conn, img_id):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    sql = ''' SELECT URL FROM IMG_URLS WHERE ID = ? '''
    cur = conn.cursor()
    cur.execute(sql, [img_id])
    rows = cur.fetchall()

    for row in rows:
        return row
