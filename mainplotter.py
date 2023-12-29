import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plots.volume_spike import get_volume_data, VolumeSpike
from plots.price_spike import get_price_data, PriceSpike
from plots.open_interest import get_oi_data, HighOI
from lib.jsonmanager import JSONManager


PLOTTER_PROPS = {
    "options": {
        "title": "Open Interest Plot",
        "xaxis_title" : "Period",
        "yaxis_title" : "Open Interest"
    },
    "equity": {
        "title": "Equity Plot",
        "xaxis_title" : "Period",
        "yaxis_title" : "Price"
    }
}

equity_filename = "jsondata/equity_data.json"
eprice_filename = "jsondata/equity_price.json"
options_filename = "jsondata/oi_data.json"

vol = go.Figure(layout={"width": 1300, "height": 600})
equity = go.Figure(layout={"width": 1300, "height": 600})
oi = go.Figure(layout={"width": 1300, "height": 600})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("MoneyMaker Charts"),

    dcc.Graph(id='oi-chart'),
    dcc.Graph(id='equity-chart'),
    dcc.Graph(id='vol-chart'),

    dcc.Interval(
        id='5min',
        interval=5 * 60 * 1000,  # in milliseconds
        n_intervals=0
    ),

    dcc.Interval(
        id='3min',
        interval=3 * 60 * 1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('oi-chart', 'figure'),
    Input('5min', 'n_intervals')
)
def update_charts(n_intervals):
    jm = JSONManager()

    high_oi = HighOI()

    oi_data = get_oi_data(options_filename, jm, high_oi.high_oi())

    oi.data = []

    for category, data in oi_data.items():
        values = [item[0] for item in data]
        times = [item[1] for item in data]
        oi.add_trace(
            go.Scatter(
                x=times,
                y=values, mode='lines+markers',
                name=f'{category} (Open Interest)'
            )
        )

    oi.update_layout(
        title=PLOTTER_PROPS["options"]["title"],
        xaxis_title=PLOTTER_PROPS["options"]["xaxis_title"],
        yaxis_title=PLOTTER_PROPS["options"]["yaxis_title"]
    )


    oi.add_annotation(
        go.layout.Annotation(
            text=str(high_oi.underlying_value),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=1.05,
            font=dict(size=14)
            )
    )

    return oi

@app.callback(
    Output('vol-chart', 'figure'),
    Output('equity-chart', 'figure'),
    Input('3min', 'n_intervals')
)
def update3_charts(n):
    jm = JSONManager()
    vs = VolumeSpike()
    ps = PriceSpike()

    volume_data = get_volume_data(equity_filename, jm, vs.volume_spike())
    price_data = get_price_data(eprice_filename, jm, ps.price_spike())

    equity.data, vol.data = [], []

    for category, values in volume_data.items():
        vol.add_trace(
            go.Scatter(
                x=list(range(1, len(values) + 1)),
                y=values, mode='lines+markers',
                name=f'{category} (Volume)'
            )
        )

    for category, values in price_data.items():
        equity.add_trace(
            go.Scatter(
                x=list(range(1, len(values) + 1)),
                y=values, mode='lines+markers',
                name=f'{category} (Price)'
            )
        )

    equity.update_layout(
        title=PLOTTER_PROPS["equity"]["title"],
        xaxis_title=PLOTTER_PROPS["equity"]["xaxis_title"],
        yaxis_title=PLOTTER_PROPS["equity"]["yaxis_title"]
    )

    vol.update_layout(
        title="Volume Plot",
        xaxis_title="Period",
        yaxis_title="Volume"
    )
    return vol, equity

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
