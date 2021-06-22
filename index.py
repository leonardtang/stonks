import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from sentiment import Sentiment
from stocks import Stocks, crop_graph_stock
from crypto import Crypto, crop_graph_crypto
from volatility import Volatility

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = 'Stonks'
server = app.server

app.config.suppress_callback_exceptions = True

# Wrapper layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/crypto':
        return Crypto()
    elif pathname == '/volatility':
        return Volatility()
    elif pathname == '/sentiment':
        return Sentiment()
    else:
        return Stocks()


@app.callback(Output("crop_graph_stock", "figure"),
              Input("ticker_drop_stock", "value"))
def update_graph_stock(ticker):
    graph = crop_graph_stock(ticker)
    return graph


@app.callback(Output("crop_graph_crypto", "figure"),
              Input("ticker_drop_crypto", "value"))
def update_graph_crypto(ticker):
    graph = crop_graph_crypto(ticker)
    return graph


# @app.callback(Output('image_wc', 'src'),
#               Input('image_wc', 'id'))
# def make_image(b):
#     img = BytesIO()
#     plot_wordcloud(data=wordcloud_df).save(img, format='PNG')
#     return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


if __name__ == '__main__':
    app.run_server(debug=True)
