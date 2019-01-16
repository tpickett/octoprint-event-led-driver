import sqlite3
import datetime
import argparse
import collections

class LEDColor():
    def __init__(this):
        #off by default
        this.color = [0,0,0]
    
    def persistColor(this, red, green, blue):
        """ Update the db with the current color were setting to """
        this.c.execute("INSERT INTO {tn} (date, red, green, blue) VALUES (DATE('now'), {red}, {green}, {blue})".\
            format(tn=this.DB_LED_TABLE, red=red, green=green, blue=blue))
        this.color = [red, green, blue]

    def getLastColor(this):
        """ returns the last color set in sqlite DB """
        this.c.execute("SELECT * FROM {tn} ORDER BY id DESC".\
            format(tn=this.DB_LED_TABLE))
        return  this.c.fetchone()