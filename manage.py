import dash

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

if __name__ == '__main__':
    app.run_server(debug=True)
