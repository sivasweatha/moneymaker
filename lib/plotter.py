import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

class Plotter:
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

    def __init__(self, data, interval="", props =PLOTTER_PROPS["options"], underlyingValue= ''):
        self.data = data
        self.props = props
        self.underlyingValue = underlyingValue
        self.interval = interval
        self.fig = go.Figure(layout={"width": 1300, "height": 600})
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div([
            html.H1("MoneyMaker Charts"),

            dcc.Graph(id='oi-chart'),

            dcc.Interval(
            id='interval-component',
            interval=self.interval * 1000,  # in milliseconds
            n_intervals=0
    )
        ])
        self.app.callback(
            Output('oi-chart', 'figure'),
            Input('interval-component', 'n_intervals')
        )(self.update_charts)

    def update_charts(self, data):
        self.data = data
        for category, values in self.data.items():
            self.fig.add_trace(
                go.Scatter(
                    x=list(range(1, len(values) + 1)),
                    y=values, mode='lines+markers',
                    name=f'{category} (Price)'
                )
            )

        self.fig.update_layout(
            title=self.props["title"],
            xaxis_title=self.props["xaxis_title"],
            yaxis_title=self.props["yaxis_title"]
        )

        self.fig.add_annotation(
            go.layout.Annotation(
                text=str(self.underlyingValue),
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0,
                y=1.05,
                font=dict(size=14)
                )
        )

        return self.fig

    def plot(self, props):

        for category, values in self.data.items():
            self.fig.add_trace(
                go.Scatter(
                    x=list(range(1, len(values) + 1)),
                    y=values, mode='lines+markers',
                    name=category
                    )
                )

        self.fig.update_layout(
            title=props["title"],
            xaxis_title=props["xaxis_title"],
            yaxis_title=props["yaxis_title"])

        if self.underlyingValue:
            self.fig.add_annotation(
                go.layout.Annotation(
                    text=str(self.underlyingValue),
                    align='left',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0,
                    y=1.05,
                    font=dict(size=14)
                    )
                )

        self.fig.show()