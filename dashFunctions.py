import datetime


from dbFunctions import create_connection, execute_sql, isInTable
from fileNames import STOCKSDBPATH
from dashSettings import *
from indicatorCalculations import *
import yfinance as yf
import MetaTrader5 as mt5
import pandas as pd

def getMostRecentData(symbol, start_date, end_date):
    packageFound = getPackageFound(symbol)

    if start_date is None or end_date is None:
        start_date = datetime.datetime.today()-datetime.timedelta(days=1)
        end_date = datetime.datetime.today()
    #if isinstance(start_date, str): start_date = datetime.datetime(start_date)
    #if isinstance(end_date, str): end_date = datetime.datetime(end_date)
    if packageFound[0] == "yfinance":
        data = yf.download(symbol, start_date, end_date, interval="5m")
    elif packageFound[0] == "Metatrader":
        mt5.initialize()
        if packageFound[1] == "Alpari":
            authorized = mt5.login(int(51086211), password='ic7hhrfb', server='Alpari-MT5-Demo')
        elif packageFound[1] == "MetaQuotes":
            authorized = mt5.login(int(56382120), password='2kgkjkmo', server="MetaQuotes-Demo")
        data = pd.DataFrame(mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, start_date, end_date))
        data['time'] = [datetime.datetime.fromtimestamp(i) for i in data['time']]
        data = data.rename(columns={
            'time': 'Datetime',
            'open': 'Open',
            'close': 'Close',
            'high': 'High',
            'low': 'Low',
            'tick_volume': 'Volume'
        }).set_index('Datetime')
    return data

def getPackageFound(symbol):
    conn = create_connection(STOCKSDBPATH)
    data = execute_sql(conn, """SELECT PackageFound, Market From Tickers WHERE Symbol like '{}' LIMIT 1""".format(symbol)).fetchall()[0]
    conn.close()
    return data

def getCalculations(data):
    candlestick = {
        'x': data.index,
        'open': data['Open'],
        'high': data['High'],
        'low': data['Low'],
        'close':data['Close']
    }
    return candlestick, movingAverage2(data['Close'], 5), exponentialMovingAverage2(data['Close'], 5)

#getMostRecentData("2022-01-24", "2022-01-26", "ETHBTC")
#exit(0)
def getCandlestickData(symbol):
    conn = create_connection(STOCKSDBPATH)
    #updateStocksDataSingle(conn, symbol)
    data = execute_sql(conn, """SELECT * FROM (SELECT Datetime, Open, High, Low, Close FROM {sym} ORDER BY Datetime DESC LIMIT 100) as temp ORDER BY Datetime ASC""".format(sym=symbol)).fetchall()
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
        data = execute_sql(conn, """SELECT * FROM (SELECT Datetime, tick_volume from {sym} ORDER BY Datetime DESC LIMIT 100) as temp ORDER BY Datetime ASC;""".format(
            sym=symbol)).fetchall()
    else:
        data = execute_sql(conn, """SELECT * FROM (SELECT Datetime, Volume from {sym} ORDER BY Datetime DESC LIMIT 100) as temp ORDER BY Datetime ASC;""".format(sym=symbol)).fetchall()
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

def getMovingAverage(symbol, n):
    conn = create_connection(STOCKSDBPATH)
    data = execute_sql(conn,
                       """SELECT * FROM (SELECT Datetime, Close FROM {sym} ORDER BY Datetime DESC LIMIT {amount}) as temp ORDER BY Datetime ASC;""".format(
                           sym=symbol, amount=str(100+n-1))).fetchall()
    data2 = {
        'x': [datetime.datetime for i in range(100+n-1)],
        'y': [0 for i in range(100+n-1)],
    }
    counter = 0
    for i in data:
        date, close = i
        data2['x'][counter] = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        data2['y'][counter] = close
        counter = counter + 1
    data2['x'] = data2['x'][n-1:]
    data2['y'] = movingAverage(data2['y'], n)
    conn.close()
    return data2

def getExponentialMovingAverage(symbol, n):
    conn = create_connection(STOCKSDBPATH)
    data = execute_sql(conn,
                       """SELECT * FROM (SELECT Datetime, Close FROM {sym} ORDER BY Datetime DESC LIMIT {amount}) as temp ORDER BY Datetime ASC;""".format(
                           sym=symbol, amount=str(100 + n - 1))).fetchall()
    data2 = {
        'x': [datetime.datetime for i in range(100 + n - 1)],
        'y': [0 for i in range(100 + n - 1)],
    }
    counter = 0
    for i in data:
        date, close = i
        data2['x'][counter] = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        data2['y'][counter] = close
        counter = counter + 1
    data2['x'] = data2['x'][n - 1:]
    data2['y'] = exponentialMovingAverage2(data2['y'], n)
    conn.close()
    return data2

def isStockInDb(symbol):
    conn = create_connection(STOCKSDBPATH)
    t = isInTable(conn, "Tickers", "Symbol", symbol)
    conn.close()
    return t

def get_newest_stocks(symbol):
    """Gets the newest stock directly from the web, without querying just the database"""

def getData(symbol):
    candlestick = getCandlestickData(symbol)
    volume = getVolume(symbol)
    sma = movingAverage()
