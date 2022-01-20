import os
from dbFunctions import get_table_names, create_connection
import pandas_market_calendars as mcal  # Get holidays
from datetime import date

STOCKSDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"StocksData")
DBDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"DataBase")
STOCKSDB = "StocksData.db"
STOCKSDBPATH = os.path.join(DBDIR, STOCKSDB)
conn = create_connection(STOCKSDBPATH)
TABLENAMES = get_table_names(conn)
conn.close()

# Gets the bank holidays
year = int(str(date.today())[:4])
HOLIDAYS = [str(i) for i in mcal.get_calendar('NYSE').holidays().holidays if year >= int(str(i)[:4]) >= 2021]
