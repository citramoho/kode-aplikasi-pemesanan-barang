import sqlite3
def createDatabase():
    try:
        sqliteConnection = sqlite3.connect('pemesanan.db')
        cursor = sqliteConnection.cursor()
        sqlite_create_table_query = '''CREATE TABLE pemesanan.db (
                            id_produk INTEGER PRIMARY KEY UNIQUE,
                            naam_produk TEXT NOT NULL,
                            harga TEXT NOT NULL,
                            jumlah TEXT NOT NULL);'''
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

def insertDatatoDB(*data):
    try:
        sqlite3Connection = sqliteConnection = sqlite3.connect('pemesanan.db')