import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from navbar import Navbar

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
wordcloud_df = pd.read_csv('data/wsb_daily_concepts.csv')

nav = Navbar()
header = dbc.Row(
    dbc.Col(
        [html.Div(
            html.H1('How is WSB Feeling Today?',
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

                        "Bull or Bear? That *is* the question."
                    ''',
                              ),
                 dcc.Link(html.Figcaption(['—A Day in the Life of an Investment Banker',
                                           html.Cite(', UBS')],
                                          ),
                          href='https://www.youtube.com/watch?v=L1qbPIfk0XI')
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

wordcloud_header = dbc.Row(
    dbc.Col([html.Div(
        html.H5('Word Cloud of Today\'s WSB Content:',
                style=
                {
                    'font-size': '1.65em',
                    'font-weight': 'bolder',
                    'color': "rgba(117, 117, 117, 0.95)",
                    'margin-top': '30px',
                    'margin-bottom': '20px',
                    "display": "block",
                    "margin-left": "auto",
                    "margin-right": "auto",
                }
                ),
        style={'textAlign': 'center'}),
    ],

    )
)

bert_header = dbc.Row(
    dbc.Col([html.Div([
        html.H5('Percentage of Positive User Submissions:',
                style=
                {
                    'font-size': '1.65em',
                    'font-weight': 'bolder',
                    'color': "rgba(117, 117, 117, 0.95)",
                    'margin-top': '30px',
                    'margin-bottom': '20px',
                    "display": "block",
                    "margin-left": "auto",
                    "margin-right": "auto",
                }
                ),
        dcc.Link(html.H5('(Classifier: XLNet Transformer Fine-Tuned on IMDB Movie Reviews)',
                         style=
                         {
                             'font-size': '1em',
                             'font-weight': 'bolder',
                             'color': "rgba(117, 117, 117, 0.95)",
                             'margin-top': '10px',
                             'margin-bottom': '20px',
                             "display": "block",
                             "margin-left": "auto",
                             "margin-right": "auto",
                         },
                         ), href='https://arxiv.org/pdf/1906.08237.pdf')
    ],
        style={'textAlign': 'center'}),
    ],

    )
)

f = open("data/sentiment_percentage.txt", "r")
portion = f.read()
portion = str(round(float(portion) * 1e2, 2)) + '%'

bert_number = dbc.Row(
    dbc.Col([html.Div(
        html.H5(portion,
                style=
                {
                    'font-size': '3.65em',
                    'font-weight': 'bolder',
                    'color': "rgba(117, 117, 117, 0.95)",
                    'margin-top': '30px',
                    'margin-bottom': '20px',
                    "display": "block",
                    "margin-left": "auto",
                    "margin-right": "auto",
                }
                ),
        style={'textAlign': 'center'}),
    ],

    )
)


def Sentiment():
    layout = nav, dbc.Container(
        [
            header,
            intro,
            bert_header,
            bert_number,
            wordcloud_header,
            html.Div([
                html.Img(id="image_wc",
                         src='assets/daily_wordcloud.png',
                         style={'width': '30%'}),
            ],
                style={'textAlign': 'center'}
            ),
        ],
        fluid=True
    )
    return layout


# def plot_wordcloud(data):
#     wsb_color = np.array(Image.open('assets/wsb_full.jpeg'))
#
#     wsb_mask = wsb_color.copy()
#     wsb_mask[wsb_mask.sum(axis=2) == 0] = 255
#     d = {a: x for a, x in data.values}
#
#     edges = np.mean([gaussian_gradient_magnitude(wsb_color[:, :, i] / 255., 2) for i in range(3)], axis=0)
#     wsb_mask[edges > .9] = 255
#     wc = WordCloud(background_color='white',
#                    mask=wsb_mask, random_state=42)
#     wc.fit_words(d)
#     image_colors = ImageColorGenerator(wsb_color)
#     wc.recolor(color_func=image_colors)
#
#     return wc.to_image()


if __name__ == '__main__':
    app.run_server(debug=True)
