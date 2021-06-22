import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from navbar import Navbar
from pandas.tseries.offsets import BDay

mentions_df = pd.read_csv('data/stock/top_stock_mentions.csv', index_col=0).iloc[1:, :]
mentions_df = mentions_df.iloc[:-1, :]
mentions_df.index = pd.to_datetime(mentions_df.index)
isBusinessDay = BDay().onOffset
match_series = pd.to_datetime(mentions_df.index).map(isBusinessDay)
mentions_df = mentions_df[match_series]

sent_df = pd.read_csv('data/historical_sentiment.csv', index_col=0)
isBusinessDay = BDay().onOffset
match_series = pd.to_datetime(sent_df.index).map(isBusinessDay)
sent_df = sent_df[match_series]

close_df = pd.read_csv('data/stock/close_stock_data.csv', index_col=0)
open_df = pd.read_csv('data/stock/open_stock_data.csv', index_col=0)
open_df.index = pd.to_datetime(open_df.index)
low_df = pd.read_csv('data/stock/low_stock_data.csv', index_col=0)
high_df = pd.read_csv('data/stock/high_stock_data.csv', index_col=0)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

nav = Navbar()

controls = dbc.Row([
    dbc.Col(

        dbc.FormGroup(
            [
                dbc.Label("Select Stock Ticker:", className="ml-1 font-weight-bold"),
                dcc.Dropdown(
                    id="ticker_drop_stock",
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
            html.H1('We Like the Stock.',
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

intro = html.Div(
    [
        html.Figure(
            html.Blockquote(
                [dcc.Markdown('''
                    
                        "I support retail investors' right to invest in what they want, when they want.
                        I support the right of individuals to send a message based on how they invest.
                        As for me, *I like the stock.*
                        I'm as bullish as I've ever been on a potential turnaround for GameStop, 
                        and I remain invested in the company.
                        Thank you, and cheers everyone."
                    ''',
                              ),
                 html.Figcaption(['—Roaring Kitty', html.Cite(', Contemporary Financial Guru')])
                 ],
                style={'textAlign': 'center'}
            ),
            style={'width': '45vw',
                   "display": "block",
                   "margin-left": "auto",
                   "margin-right": "auto",
                   'background': '#f9f9f9',
                   'border-left': '7px solid #ccc',
                   'padding-top': '0.5em',
                   'padding-left': '0.5em',
                   'padding-right': '0.5em',
                   'padding-bottom': '0.05em'
                   },
        )

    ],
)

graph = dbc.Col([
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="crop_graph_stock",
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


def Stocks():
    layout = nav, dbc.Container(
        [
            header,
            intro,
            controls,
            graph
        ],
        fluid=True
    )
    return layout


def crop_graph_stock(ticker):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(name='WSB Mentions',
                             x=open_df.index,
                             y=mentions_df[ticker],
                             mode='lines',
                             line=dict(color='navy', width=1.3)),
                  secondary_y=True,
                  )

    fig.add_trace(go.Candlestick(name='Share Price',
                                 x=open_df.index,
                                 open=open_df[ticker], high=high_df[ticker],
                                 low=low_df[ticker], close=close_df[ticker]),
                  secondary_y=False
                  )

    # fig.update_layout(xaxis_tickformat='%')

    fig['layout']['yaxis1']['showgrid'] = False
    fig.update_yaxes(title_text="<b>US Dollars</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Mentions Per Day</b>", secondary_y=True)

    # fig.update_layout(template="plotly_dark", plot_bgcolor='#272B30', paper_bgcolor='#272B30')
    fig.update_layout(margin_r=20)
    fig.update_layout(margin_pad=10)
    fig.update_layout(hovermode='x')
    fig.update_layout(showlegend=True,
                      legend=dict(yanchor="top",
                                  y=0.99,
                                  xanchor="left",
                                  x=0.01
                                  )
                      )
    fig.update_layout(title_text=f'WSB Mentions vs. ${ticker} Historical Price', title_x=0.5)
    fig.update_layout(autosize=True)

    # fig.update_layout(xaxis={'tickformat': '%y/%m'})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
