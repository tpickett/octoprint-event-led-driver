import sqlite3
import datetime
import argparse
import collections

LEDRecord = collections.namedtuple('LEDRecord', 'id date red green blue')
def namedtuple_factory(cursor, row):
    return LEDRecord(*row)

class LEDDriverDB:
    def __init__(this):
        this.connect()


    def connect(this):
        """ Make connection to an SQLite database file """
        this.conn = sqlite3.connect(this.DB_FILE)
        this.conn.row_factory = namedtuple_factory
        this.c = this.conn.cursor()
        this.checkDbSetup()


    def close(this):
        """ Commit changes and close connection to the database """
        this.conn.commit()
        this.conn.close()
        return

    def checkDbSetup(this):
        """ Verifies that the Database had the tables and columns configured """
        this.c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, red INTEGER, green INTEGER, blue INTEGER)'\
            .format(tn=this.DB_LED_TABLE))