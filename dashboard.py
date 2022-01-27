import datetime
import dash
from dash import dcc
from dash import html
import plotly
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dashFunctions import getCandlestickData, getVolume, isStockInDb, getMovingAverage, getExponentialMovingAverage, getMostRecentData, getCalculations
from dashSettings import *
from time import sleep



app = dash.Dash(__name__)

app.layout = html.Div(
    children=[html.Div([
        html.H4(children="", id="first-stock-name"),
        dcc.Input(id="first-stock-input", placeholder="Stock Symbol Here"),
        dcc.DatePickerRange(id="date-range-1"),
        dcc.Graph(id='first-graph'),
        html.H4(children="", id="second-stock-name"),
        dcc.Input(id="second-stock-input", placeholder="Stock Symbol Here"),
        dcc.Graph(id='second-graph'),
        dcc.Store(id='curr-graph1-symbol', data='EURUSD'),
        dcc.Store(id='curr-graph2-symbol', data='AAPL'),
        dcc.Interval(
            id='interval-component',
            interval=20*1000, # in milliseconds
            n_intervals=0
        )
    ])]
)


@app.callback([Output('first-graph', 'figure'),
               Output('second-graph', 'figure'),
               Output('first-stock-name', 'children'),
               Output('second-stock-name', 'children'),
               Output('curr-graph1-symbol', 'data'),
               Output('curr-graph2-symbol', 'data')],
              [Input('interval-component', 'n_intervals'),
               Input('first-stock-input', "value"),
               Input('second-stock-input', "value"),
               Input('curr-graph1-symbol', 'data'),
               Input('curr-graph2-symbol', 'data'),
               Input('date-range-1', 'start_date'),
               Input('date-range-1', 'end_date')
               ])
def update_graph(n, firstSymbol, secondSymbol, curr1symbol, curr2symbol,start_date, end_date):
    if not isStockInDb(firstSymbol):
        firstSymbol = curr1symbol
    if not isStockInDb(secondSymbol):
        secondSymbol = curr2symbol

    if start_date is None or end_date is None:
        start_date = datetime.datetime.today() - datetime.timedelta(days=1)
        end_date = datetime.datetime.today()
    else:
        start_date = start_date.split("-")
        end_date = end_date.split("-")
        start_date = datetime.datetime(year=int(start_date[0]),month=int(start_date[1]), day=int(start_date[2]))
        end_date = datetime.datetime(year=int(end_date[0]),month=int(end_date[1]), day=int(end_date[2]))
    data = getMostRecentData(firstSymbol, start_date, end_date)
    print(data)
    candlestick, sma, ema = getCalculations(data)


    #candleStick=getCandlestickData(firstSymbol)

    fig1=make_subplots(specs=[[{"secondary_y":True}]])
    fig1.add_trace(go.Candlestick(candlestick), secondary_y=True)
    fig1.add_trace(go.Bar(x=data.index, y=data['Volume'],opacity=0.5,), secondary_y=False)
    fig1.add_trace(go.Line(x=data.index, y=sma), secondary_y=True)
    fig1.add_trace(go.Line(x=data.index, y=ema), secondary_y=True, )
    fig1.update_layout(graph_layout)
    fig1.update_layout(yaxis_range=[0,2*max(data['Volume'])], showlegend=False)
    data2 = getVolume(secondSymbol)
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Candlestick(**getCandlestickData(secondSymbol)),
        secondary_y=True)
    fig2.add_trace(go.Bar(x=data2['x'], y=data2['y'], opacity=0.5, ), secondary_y=False)
    fig2.update_layout(graph_layout)
    fig2.update_layout(yaxis_range=[0, 2 * max(data2['y'])], showlegend=False)

    return (fig1,
            fig2,
            firstSymbol,
            secondSymbol,
            firstSymbol,
            secondSymbol)



if __name__ == '__main__':
    app.run_server(debug=True)
