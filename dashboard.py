import datetime
import dash
from dash import dcc
from dash import html
import plotly
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from getStocks import getStockLocal
from fileNames import HOLIDAYS
from dashFunctions import getSymbol
from dashSettings import *
from dbFunctions import create_connection, execute_sql


app = dash.Dash(__name__)

app.layout = html.Div(
    children=[html.Div([
        html.H4(children="", id="first-stock-name"),
        dcc.Input(id="first-stock-input", placeholder="Stock Symbol Here"),
        dcc.Graph(id='first-graph'),
        html.H4(children="", id="second-stock-name"),
        dcc.Input(id="second-stock-input", placeholder="Stock Symbol Here"),
        dcc.Graph(id='second-graph'),
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        )
    ])]
)


@app.callback([Output('first-graph', 'figure'),
                Output('second-graph', 'figure'),
               Output('first-stock-name', 'children'),
               Output('second-stock-name', 'children')],
              [Input('interval-component', 'n_intervals'),
               Input('first-stock-input', "value"),
               Input('second-stock-input', "value")])
def update_graph(n, firstSymbol, secondSymbol):
    if firstSymbol is None or len(firstSymbol) == 0:
        firstSymbol = "EURUSD"
    if secondSymbol is None or len(secondSymbol) == 0:
        secondSymbol = "AAPL"

    return (go.Figure(data=go.Candlestick(**getSymbol(firstSymbol),decreasing_line_color='green', increasing_line_color='red'),layout=graph_layout),
           go.Figure(data=go.Candlestick(**getSymbol(secondSymbol),decreasing_line_color='green', increasing_line_color='red'), layout=graph_layout),
           firstSymbol,
           secondSymbol)



if __name__ == '__main__':
    app.run_server(debug=True)
