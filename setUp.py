from yahoo_fin import stock_info as si
from fileNames import *
import sqlite3
from dbFunctions import *
import MetaTrader5 as mt5



tickers_sp500 = ["'"+i+"'" for i in si.tickers_sp500()]
Market = ["'SP500'" for i in tickers_sp500]
tickers_nasdaq = ["'"+i+"'" for i in si.tickers_nasdaq()]
Market = Market + ["'NASDAQ'" for i in tickers_nasdaq]
tickers_dow = ["'"+i+"'" for i in si.tickers_dow()]
Market = Market + ["'DOW'" for i in tickers_dow]
if not os.path.exists(DBDIR):
    os.mkdir(DBDIR)
db_file = os.path.join(DBDIR, STOCKSDB)  # Path to DB file
print(db_file)
conn = create_connection(db_file)  # create tge database and the connection
execute_sql(conn, create_table_command("Tickers", ["Symbol", "Market", "PackageFound"], ["Text","Text","Text"]))
values = zip(tickers_sp500+tickers_nasdaq+tickers_dow, Market, ["'yfinance'" for i in Market])
execute_sql(conn, insert_into_command("Tickers", ["Symbol", "Market", "PackageFound"], values), commit=True)


# Metatrader forex
# Username: 56382120
# Password: 2kgkjkmo
# Investor: m5evdehj
# Metatrader s&p500
# Username: 51086211
# Password: ic7hhrfb
# Investor: rztk4kja
account = int(51086211)
mt5.initialize()
authorized=mt5.login(account, password='ic7hhrfb', server='Alpari-MT5-Demo')
symbols1 = mt5.symbols_get()
symbols1 = ["'"+i.name+"'" for i in symbols1]
Market = ["'Alpari'" for i in symbols1]
packageFound = ["'Metatrader'" for i in symbols1]

authorized_basic = mt5.login(56382120, password='2kgkjkmo', server="MetaQuotes-Demo")
symbols2 = mt5.symbols_get()
symbols2 = ["'"+i.name+"'" for i in symbols2]
Market = Market + ["'MetaQuotes'" for i in symbols1]
packageFound = packageFound + ["'Metatrader'" for i in symbols1]
values = zip(symbols1+symbols2, Market, packageFound)
execute_sql(conn, insert_into_command("Tickers", ["Symbol", "Market", "PackageFound"], values), commit=True)

conn.close()

exit(0)
stockSymbols = set(si.tickers_sp500() + si.tickers_nasdaq() + si.tickers_dow() + si.tickers_other() + si.tickers_niftybank() + \
si.tickers_ftse100() + si.tickers_ftse250() + si.tickers_ibovespa() + si.tickers_nifty50())

if not os.path.exists(STOCKSDIR):
    os.mkdir(STOCKSDIR)

for stockSymbol in stockSymbols:
    stockSymbol = stockSymbol.split("$")[0]
    if not os.path.isfile(os.path.join(STOCKSDIR, stockSymbol)) or not os.path.isdir(os.path.join(STOCKSDIR, stockSymbol)):
        if len(stockSymbol) > 0:
            try:
                os.mkdir(os.path.join(STOCKSDIR, stockSymbol))
            except FileExistsError:
                print(stockSymbol, os.path.isfile(os.path.join(STOCKSDIR, stockSymbol)), os.path.isdir(os.path.join(STOCKSDIR, stockSymbol)))
