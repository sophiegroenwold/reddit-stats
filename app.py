import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, State, Input

import pandas as pd

import data

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

hot_df = data.hot('UCSantaBarbara')
new_df = data.new('UCSantaBarbara')
name = data.name('UCSantaBarbara')
description = data.description('UCSantaBarbara')
num_subscribers = data.num_subscribers('UCSantaBarbara')
time_created = data.time_created('UCSantaBarbara')
top_users_day_df = data.top_users('UCSantaBarbara', 'day')

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

    html.Div(children=[
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
])

# app.layout = html.Div([
#     # represents the URL bar, doesn't render anything
#     dcc.Location(id='url', refresh=False),

#     html.H1(children='redditometer'),
#     html.Div('Enter the name of a subreddit to view stats and toxicity.'),

#     # for link
#     # dcc.Link('Navigate to /UCSantaBarbara', href='/UCSantaBarbara'),
#     # html.Div(id='page-content')

#     # for input box
#     # dcc.Input(id='input_subreddit_id', type='text'),
#     # html.Div(id='input_subreddit_div')
# ])

# for link
# @app.callback(dash.dependencies.Output('page-content', 'children'),
#               [dash.dependencies.Input('url', 'pathname')])

# for input box
# @app.callback(
#     Output(component_id='input_subreddit_div', component_property='children'),
#     [Input(component_id='input_subreddit_id', component_property='value')]
# )

# def display_page(input):
#     hot_df = data.hot('UCSantaBarbara')
#     new_df = data.new('UCSantaBarbara')
#     name = data.name('UCSantaBarbara')
#     description = data.description('UCSantaBarbara')
#     num_subscribers = data.num_subscribers('UCSantaBarbara')
#     time_created = data.time_created('UCSantaBarbara')
#     top_users_day_df = data.top_users('UCSantaBarbara', 'day')

#     # if pathname == '/':
#     #     return html.Div('')

#     # else:
#     return html.Div(children=[
#         html.Div(className = "parent_left", children = 
#             html.Div(className = "quick_stats", children=[
#                 html.H2('quick stats'),

#                 # subreddit basic info
#                 html.Div('Welcome to ', className = 'div_no_new_line'),
#                 html.A('r/' + name, href = 'https://www.reddit.com/r/' + name, className = "no_newline", target = "_blank"),
#                 html.Div(description),
#                 html.Div(str(num_subscribers) + ' subscribers'),
#                 html.Div('Created ' + time_created),

#                 # hot posts
#                 html.H3('hot posts'),
#                 # generate_list(hot_df),

#                 # top posts
#                 html.H3('new posts'),
#                 generate_list(new_df), 
                
#                 # top users of the day
#                 html.H3('top users'),
#                 generate_table(top_users_day_df)
#             ])
#         )
#     ])

if __name__ == '__main__':
    app.run_server(debug=True)