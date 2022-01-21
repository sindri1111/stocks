import datetime
import dash
from dash import dcc
from dash import html
import plotly
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dashFunctions import getCandlestickData, getVolume, isStockInDb
from dashSettings import *




app = dash.Dash(__name__)

app.layout = html.Div(
    children=[html.Div([
        html.H4(children="", id="first-stock-name"),
        dcc.Input(id="first-stock-input", placeholder="Stock Symbol Here"),
        dcc.Graph(id='first-graph'),
        html.H4(children="", id="second-stock-name"),
        dcc.Input(id="second-stock-input", placeholder="Stock Symbol Here"),
        dcc.Graph(id='second-graph'),
        dcc.Store(id='curr-graph1-symbol', data='EURUSD'),
        dcc.Store(id='curr-graph2-symbol', data='AAPL'),
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
               Output('second-stock-name', 'children'),
               Output('curr-graph1-symbol', 'data'),
               Output('curr-graph2-symbol', 'data')],
              [Input('interval-component', 'n_intervals'),
               Input('first-stock-input', "value"),
               Input('second-stock-input', "value"),
               Input('curr-graph1-symbol', 'data'),
               Input('curr-graph2-symbol', 'data')])
def update_graph(n, firstSymbol, secondSymbol, curr1symbol, curr2symbol):
    if not isStockInDb(firstSymbol):
        firstSymbol = curr1symbol
    if not isStockInDb(secondSymbol):
        secondSymbol = curr2symbol
    data1=getVolume(firstSymbol)
    fig1=make_subplots(specs=[[{"secondary_y":True}]])
    fig1.add_trace(go.Candlestick(**getCandlestickData(firstSymbol),decreasing_line_color='green', increasing_line_color='red'), secondary_y=True)
    fig1.add_trace(go.Bar(x=data1['x'], y=data1['y'],opacity=0.5,), secondary_y=False)
    fig1.update_layout(graph_layout)
    fig1.update_layout(yaxis_range=[0,2*max(data1['y'])], showlegend=False)
    data2 = getVolume(secondSymbol)
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Candlestick(**getCandlestickData(secondSymbol), decreasing_line_color='green', increasing_line_color='red'),
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
