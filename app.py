import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, State, Input

import pandas as pd

import data

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def generate_list(dataframe):
    return html.Div([
        html.A(dataframe.iloc[i][0], href = dataframe.iloc[i][1], className = "newline", target = "_blank") for i in range(len(dataframe))
    ])

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    html.H1(children='redditometer'),
    html.Div('Enter the name of a subreddit to view stats and toxicity.'),

    dcc.Input(id="input", type="text", placeholder="", debounce=True),
    html.Div(id="output")
])

@app.callback(
    Output("output", "children"),
    [Input("input", "value")],
)

def update_output(input):
    query = str(input)
    if (query == 'None'):
        return html.Div(children=[])
    else:
        hot_df = data.hot(query)
        new_df = data.new(query)
        name = data.name(query)
        description = data.description(query)
        num_subscribers = data.num_subscribers(query)
        time_created = data.time_created(query)
        top_users_day_df = data.top_users(query, 'day')

        return html.Div(children=[
            html.Div(className = "parent_left", children = 
                html.Div(className = "quick_stats", children=[
                    html.H2('quick stats'),

                    # subreddit basic info
                    html.Div('Welcome to ', className = 'div_no_new_line'),
                    html.A('r/' + name, href = 'https://www.reddit.com/r/' + name, className = "no_newline", target = "_blank"),
                    html.Div(description),
                    html.Div(str(num_subscribers) + ' subscribers'),
                    html.Div('Created ' + time_created),

                    # hot posts
                    html.H3('hot posts'),
                    generate_list(hot_df),

                    # top posts
                    html.H3('new posts'),
                    generate_list(new_df), 
                    
                    # top users of the day
                    html.H3('top users'),
                    generate_table(top_users_day_df)
                ])
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)