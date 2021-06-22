import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from navbar import Navbar

total_mentions = pd.read_csv('data/volatility/total_wsb_mentions.csv', index_col=0)
total_mentions.index = pd.to_datetime(total_mentions.index)
spy_vol = pd.read_csv('data/volatility/total_market_volume.csv', index_col=0)
vix = pd.read_csv('data/volatility/historical_vix.csv', index_col=0)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

nav = Navbar()

header = dbc.Row(
    dbc.Col(
        [html.Div(
            html.H1('Retail Investors Don\'t Matter.',
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

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Plotting price without candlestick:
fig.add_trace(go.Scatter(name='VIX Close',
                         x=total_mentions.index,
                         y=vix['CLOSE'],
                         mode='lines',
                         line=dict(color="maroon", width=1)
                         ),
              secondary_y=False
              )

fig.add_trace(go.Scatter(name='Total WSB Submissions',
                         x=total_mentions.index,
                         y=total_mentions['Total Mentions'],
                         mode='lines',
                         line=dict(color='navy', width=1.3)),
              secondary_y=True,
              )

# fig.add_trace(go.Candlestick(name='VIX Price',
#                              x=vix[ticker].index,
#                              open=open_df[ticker], high=high_df[ticker],
#                              low=low_df[ticker], close=close_df[ticker]),
#               secondary_y=False
#               )

fig['layout']['yaxis1']['showgrid'] = False
fig.update_yaxes(title_text="<b>CBOE Volatility Index</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>Submissions Per Day</b>", secondary_y=True)

# fig.update_layout(template="plotly_dark", plot_bgcolor='#272B30', paper_bgcolor='#272B30')
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
fig.update_layout(title_text=f'Total WSB Activity vs. VIX', title_x=0.5)
fig.update_layout(autosize=True)

intro = html.Div(
    [
        html.Figure(
            html.Blockquote(
                [dcc.Markdown('''
                        "The individual investor should act consistently as an investor and not as a speculator." 
                    ''',
                              ),
                 html.Figcaption(['—Benjamin Graham', html.Cite(', A Second-Rate Roaring Kitty')])
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
            dcc.Graph(id="graph_volatility",
                      figure=fig,
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


def Volatility():
    layout = nav, \
             dbc.Container(
                 [
                     header,
                     intro,
                     graph
                 ],
                 fluid=True
             )
    return layout


# @app.callback(Output("graph_volatility", "figure"),
#               Input(""))
# def graph_volatility():


if __name__ == '__main__':
    app.run_server(debug=True)
