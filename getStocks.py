import yfinance as yf
import datetime
from datetime import timedelta
from fileNames import *
from dbFunctions import *
import MetaTrader5 as mt5

# pdr api key = pnVctwYEPg7jnxERoz6u

def getStock(conn, symbol, time_start, time_end, interval="5m", save=False, skip_if_in_db=False, tablenames=None):
    print("Getting stock: ", symbol)
    ret = execute_sql(conn, "SELECT Symbol, Market, PackageFound From Tickers WHERE Symbol like '{}'".format(symbol))
    data = []
    for value in ret.fetchall():

        if value[2] == "yfinance":
            stock = value[0]
            data = yf.download(stock, time_start, time_end, interval=interval)
            if not data.empty:
                if save:
                    if stock not in TABLENAMES:
                        create_table_cmd = """CREATE TABLE IF NOT EXISTS "{tablename}" (
                        id integer PRIMARY KEY,
                        Datetime DATETIME UNIQUE,
                        Open FLOAT,
                        High FLOAT,
                        Low FLOAT,
                        Close FLOAT,
                        "Adj Close" FLOAT,
                        Volume FLOAT
                        )
                        """.format(tablename=stock)
                        execute_sql(conn, create_table_cmd)
                    counter = 0
                    cmd = """INSERT OR IGNORE INTO "{}" \n""".format(stock)
                    for line in data.to_csv().split("\n"):
                        line = line.strip()
                        if counter == 0:
                            cmd = cmd + "(" + ",".join(['"' + i + '"' for i in line.split(",")]) + ")\n VALUES"
                            counter = 1
                        elif len(line) > 0:
                            if ",," not in line:
                                line = line.split(",")
                                line[0] = "'" + "-".join(line[0].split("-")[:-1]) + "'"
                                cmd = cmd + "(" + ",".join(line) + "),\n"
                    #print(cmd.strip()[:-1])
                    cmd = cmd.strip()[:-1]
                    execute_sql(conn, cmd, commit=True)
                break
        elif value[2] == "Metatrader":
            stock = value[0]
            mt5.initialize()
            if value[1] == "Alpari":
                authorized = mt5.login(int(51086211), password='ic7hhrfb', server='Alpari-MT5-Demo')
            elif value[1] == "MetaQuotes":
                authorized = mt5.login(int(56382120), password='2kgkjkmo', server="MetaQuotes-Demo")
            data = mt5.copy_rates_range(stock, mt5.TIMEFRAME_M5, time_start, time_end)
            if len(data) > 0:
                if save:
                    if stock not in TABLENAMES:
                        create_table_cmd = """CREATE TABLE IF NOT EXISTS "{tablename}" (
                        id integer PRIMARY KEY,
                        Datetime DATETIME UNIQUE,
                        Open FLOAT,
                        High FLOAT,
                        Low FLOAT,
                        Close FLOAT,
                        tick_volume FLOAT,
                        spread FLOAT,
                        real_volume FLOAT
                        )
                        """.format(tablename=stock)
                        execute_sql(conn, create_table_cmd)

                    cmd = """INSERT OR IGNORE INTO "{}" (Datetime, Open, High, Low, Close, tick_volume, spread, real_volume) VALUES\n""".format(stock)
                    for line in data:
                        cmd = cmd + "(" + "'" + str(datetime.datetime.fromtimestamp(line[0])) + "'," + ",".join(list([str(kkk) for kkk in line])[1:]) + "),\n"
                    cmd = cmd[:-2]
                    execute_sql(conn, cmd, commit=True)
                break
    return data

def getAllStocks():
    """Gets all stocks within the last 60 days at 5 minute intervals, called on initial set up"""
    conn = create_connection(STOCKSDBPATH)
    for symbol in list(set([i[0] for i in execute_sql(conn, """SELECT DISTINCT Symbol FROM Tickers""").fetchall()])):
        getStock(conn, symbol, datetime.datetime.today() - timedelta(days=59), datetime.datetime.today(), save=True)
    conn.close()

def updateStocksDataSingle(conn, symbol):
    """Updates a single stock"""
    start_date = execute_sql(conn, """SELECT Datetime FROM "{}" ORDER BY Datetime DESC LIMIT 1""".format(symbol)).fetchall()[0][0]
    end_date = datetime.datetime.today()
    getStock(conn, symbol, datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S"), end_date, save=True)

def fixStockFailToday():
    conn = create_connection(STOCKSDBPATH)
    start_date = datetime.date.today() - timedelta(days=1)
    end_date = datetime.date.today()
    total = len(list(set([i[0] for i in execute_sql(conn, """SELECT DISTINCT Symbol FROM Tickers""").fetchall()])))
    counter = 0
    for symbol in list(set([i[0] for i in execute_sql(conn, """SELECT DISTINCT Symbol FROM Tickers""").fetchall()])):
        try:
            getStock(conn, symbol, start_date, end_date, save=True)
        except:
            pass
        print("Fixing failed stocks: ", counter/total*100, "% Complete")
        counter = counter + 1
    conn.close()

def updateStocksData():
    """Goes through all tables and gets the newest data, runs once a day"""
    conn = create_connection(STOCKSDBPATH)
    total = len(list(set([i[0] for i in execute_sql(conn, """SELECT DISTINCT Symbol FROM Tickers""").fetchall()])))
    counter = 0
    for symbol in list(set([i[0] for i in execute_sql(conn, """SELECT DISTINCT Symbol FROM Tickers""").fetchall()])):
        updateStocksDataSingle(conn, symbol)
        print("Updating Stocks: ", counter / total * 100, "% Complete")
        counter = counter + 1
    conn.close()

def getOneDay(symbol, date):
    """Gets the stock for one day of a symbol"""
    conn = create_connection(STOCKSDBPATH)

    data = execute_sql(conn,
                       """SELECT * FROM "{symbol}" WHERE Datetime BETWEEN '{date} 00:00' AND '{date} 23:59'
                       """.format(symbol=symbol, date=str(date))).fetchall()
    conn.close()
    return data

def getStockLocal(conn, symbol, time_start, time_end):
    """Gets the stocks data from the database"""
    print("""SELECT * FROM {} WHERE Datetime BETWEEN '{}' AND '{}'""".format(symbol, time_start, time_end))
    return execute_sql(conn, """SELECT * FROM {} WHERE Datetime BETWEEN '{}' AND '{}'""".format(symbol, time_start, time_end)).fetchall()

def getAllTableNames():
    conn = create_connection(STOCKSDBPATH)
    tablenames = get_table_names(conn)
    conn.close()
    return tablenames

def download_one_at_a_time_WORKING():
    """Puts in CSV file - slow"""
    for stock in os.listdir(STOCKSDIR):

        if stock < "FLN":
            pass
        else:
            for i in range(29):
                date_high = datetime.date.today() - timedelta(days=i+1)
                date_low = datetime.date.today() - timedelta(days=i)
                filepath = os.path.join(STOCKSDIR, stock, "StockData" + str(date_low).replace("-", "") + ".csv")
                if not os.path.exists(filepath):
                    data = yf.download(stock,str(date_high), date_low, interval="1m")
                    if not data.empty:
                        data.to_csv(filepath)


def deprecated_download_all():
    symb = list(os.listdir(STOCKSDIR))
    keys = ['Low', 'Volume', 'Adj Close', 'Close', 'Open', 'High']
    for i in range(29):
        date_high = datetime.date.today() - timedelta(days=i + 1)
        date_low = datetime.date.today() - timedelta(days=i)
        data = yf.download(symb,str(date_high), date_low, interval="1m")
        for sym in symb:
            filepath = os.path.join(STOCKSDIR, sym, "StockData" + str(date_low).replace("-", "") + ".csv")
            if not os.path.isfile(filepath):
                data[[(i, sym) for i in keys]].to_csv(filepath)

