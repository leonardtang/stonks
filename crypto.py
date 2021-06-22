import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
import plotly.graph_objs as go
from pandas.tseries.offsets import BDay
from plotly.subplots import make_subplots
from navbar import Navbar

mentions_df = pd.read_csv('data/crypto/top_crypto_mentions.csv', index_col=0)
close_df = pd.read_csv('data/crypto/close_crypto_data.csv', index_col=0)
open_df = pd.read_csv('data/crypto/open_crypto_data.csv', index_col=0)
open_df.index = pd.to_datetime(open_df.index)
low_df = pd.read_csv('data/crypto/low_crypto_data.csv', index_col=0)
high_df = pd.read_csv('data/crypto/high_crypto_data.csv', index_col=0)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

nav = html.Div(Navbar(), style={'width': '100%'})

controls = dbc.Row([
    dbc.Col(

        dbc.FormGroup(
            [
                dbc.Label("Select Crypto Ticker:", className="ml-1 font-weight-bold"),
                dcc.Dropdown(
                    id="ticker_drop_crypto",
                    options=[
                        {"label": col, "value": col} for col in mentions_df.columns
                    ],
                    value=mentions_df.columns[0],
                )
            ],
        ),

    ),

])

header = dbc.Row(
    dbc.Col(
        [html.Div(
            html.H1('We Like the Coin.',
                    style=
                    {
                        'font-size': '2.65em',
                        'font-weight': 'bolder',
                        'color': "rgba(117, 117, 117, 0.95)",
                        'margin-top': '20px',
                        'margin-bottom': '0',
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    }
                    ),
            style={'textAlign': 'center'}),
            html.Hr(),
        ],
    )
)

graph = dbc.Col([
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="crop_graph_crypto",
                      config={
                          'displayModeBar': False
                      },
                      style={'width': '90vw',
                             # 'height': '70vh',
                             "display": "block",
                             "margin-left": "auto",
                             "margin-right": "auto",
                             },
                      ),
        )
    ])
])

doge_img = dbc.Col([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Figure([
                    html.Img(src='assets/doge.png',
                             style={'width': '20%'}),
                    html.Figcaption([html.Cite('Doge: National Treasure')],
                                    style={'margin-top': '0.75em'}
                                    )
                ],
                )
            ],
                style={'textAlign': 'center', 'margin-bottom': '10px'}
            )
        )]
    )
])


def Crypto():
    layout = nav, \
             dbc.Container(
                 [
                     header,
                     doge_img,
                     controls,
                     graph
                 ],
                 fluid=True
             )
    return layout


def crop_graph_crypto(ticker):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(name=f'{ticker} Mentions',
                             x=open_df.index,
                             y=mentions_df[ticker],
                             mode='lines',
                             line=dict(color='navy', width=1.3)),
                  secondary_y=True,
                  )

    fig.add_trace(go.Candlestick(name='Coin Price',
                                 x=open_df.index,
                                 open=open_df[ticker], high=high_df[ticker],
                                 low=low_df[ticker], close=close_df[ticker]),
                  secondary_y=False
                  )

    fig['layout']['yaxis1']['showgrid'] = False
    fig.update_yaxes(title_text="<b>US Dollars</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Mentions Per Day</b>", secondary_y=True)

    fig.update_layout(margin_r=20)
    fig.update_layout(margin_pad=10)
    fig.update_layout(hovermode='x')
    fig.update_layout(showlegend=True,
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="left",
                          x=0.01
                      )
                      )
    fig.update_layout(title_text=f'WSB Mentions vs. ${ticker} Historical Price', title_x=0.5)
    fig.update_layout(autosize=True)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
