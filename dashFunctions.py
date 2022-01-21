import datetime

import dash
from dash import dcc
from dash import html
import plotly
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from getStocks import getStockLocal, updateStocksDataSingle
from dbFunctions import create_connection, execute_sql, isInTable
from fileNames import STOCKSDBPATH
from dashSettings import *
import 


def getCandlestickData(symbol):
    conn = create_connection(STOCKSDBPATH)
    #updateStocksDataSingle(conn, symbol)
    data = execute_sql(conn, """SELECT Datetime, Open, High, Low, Close FROM {sym} ORDER BY Datetime DESC LIMIT 100""".format(sym=symbol)).fetchall()
    # getStockLocal(conn, "AAPl", datetime.date.today() + datetime.timedelta(hours=9, minutes=30), datetime.datetime.today())
    data2 = {
        'x': [datetime.datetime for i in range(100)],
        'open': [0 for i in range(100)],
        'high': [0 for i in range(100)],
        'low': [0 for i in range(100)],
        'close': [0 for i in range(100)]
    }
    counter = 0
    for i in data:
        date, Open, High, Low, Close = i
        data2['x'][counter] = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        data2['open'][counter] = Open
        data2['high'][counter] = High
        data2['low'][counter] = Low
        data2['close'][counter] = Close
        counter = counter + 1
    conn.close()
    return data2

def getVolume(symbol):
    conn = create_connection(STOCKSDBPATH)
    packageFound = execute_sql(conn, """SELECT PackageFound FROM Tickers WHERE Symbol='{sym}' LIMIT 1;""".format(sym=symbol)).fetchall()[0][0]
    if packageFound == "Metatrader":
        data = execute_sql(conn, """SELECT Datetime, tick_volume from {sym} ORDER BY Datetime DESC LIMIT 100""".format(
            sym=symbol)).fetchall()
    else:
        data = execute_sql(conn, """SELECT Datetime, Volume from {sym} ORDER BY Datetime DESC LIMIT 100""".format(sym=symbol)).fetchall()
    data2 = {
        'x': [datetime.datetime for i in range(100)],
        'y': [0 for i in range(100)],
    }
    counter = 0
    for i in data:
        date, volume = i
        data2['x'][counter] = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        data2['y'][counter] = volume
        counter = counter + 1
    conn.close()
    return data2

def isStockInDb(symbol):
    conn = create_connection(STOCKSDBPATH)
    t = isInTable(conn, "Tickers", "Symbol", symbol)
    conn.close()
    return t

def get_newest_stocks(symbol):
    """Gets the newest stock directly from the web, without querying just the database"""
