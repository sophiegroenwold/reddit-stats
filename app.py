import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

import data

hot_df = data.hot()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# def generate_list(dataframe, max_rows=10):
#     return html.Table([
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])


def generate_list(dataframe):
    return html.Div([
        html.A(dataframe.iloc[i][0], href = dataframe.iloc[i][1], className = "newline", target = "_blank") for i in range(len(dataframe))
    ])

app.layout = html.Div(children=[
    html.H1(children='Reddit Statistics'),

    # html.Div(children='''
    #     Dash: A web application framework for Python.
    # '''),

    # hot posts
    generate_list(hot_df)
])

if __name__ == '__main__':
    app.run_server(debug=True)