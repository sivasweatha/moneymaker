import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from lib.jsonmanager import JSONManager
from vendors.nse import NSE
import pandas as pd
from datetime import datetime as dt

class Equity:
    def __init__(self) -> None:
        nse = NSE()
        self.df = nse.equity()

    def equity(self):
        df = self.df.drop(
            ['open',
            'dayHigh',
            'dayLow',
            'lastPrice',
            'previousClose',
            'totalTradedValue'],
            axis="columns")
        df['time'] = str(dt.now().strftime("%H:%M"))
        return df

def get_volume_data(filename, jm, volume_data, write=True):
    data = jm.read_data(filename)
    for index, row in volume_data.iterrows():
        stock = str(index)
        stock_data = data.setdefault(stock, {})
        stock_data.setdefault("volume", []).append(row['totalTradedVolume'])
        stock_data.setdefault("change", []).append(row['change'])
        stock_data.setdefault("time", []).append(row['time'])
    if write:
        jm.write_data(filename, data)
    return data

def run_data(write=True):
    e = Equity()
    if write:
        data = get_volume_data(filename, jm, e.equity())
    else:
        data = get_volume_data(filename, jm, e.equity(), False)

    figs = {stock: go.Figure(layout={"width": 1300, "height": 600}) for stock in data}
    graphs = [dcc.Graph(id=stock) for stock in data]
    outputs = [Output(stock, "figure") for stock in data]
    return figs, graphs, outputs, data

filename = "jsondata/stock_individual_data.json"
jm = JSONManager()
figs, graphs, outputs, equity_data = run_data(False)
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("MoneyMaker Charts", id="h1"),

    dcc.Interval(
        id='3min',
        interval=3 * 60 * 1000,
        n_intervals=0
    ),
] + graphs)

@app.callback(
    *outputs,
    Input('3min', "n_intervals")
)
def update_charts(n_interval):
    figs, graphs, outputs, equity_data = run_data()
    for name, fig in figs.items():
        fig.data = []
        data = equity_data[name]
        fig.add_trace(
            go.Scatter(
                x=data['time'],
                y=data['change'],
                yaxis="y",
                mode='lines+markers',
                name='Change'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=data['time'],
                y=data['volume'],
                yaxis="y2",
                mode='lines+markers',
                name='Volume'
            )
        )

        fig.update_layout(
            title=name,
            xaxis_title="Time",
            yaxis_title="Change",
            yaxis2 = dict(title='Volume', overlaying='y', side='right')
        )

    return list(figs.values())

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port="5080")