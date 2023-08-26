
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import io
import base64
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = [
    ['Syed', 'Syed@123'],
    ['Sachin', 'Sachin@123'],
    ['Abhishek', 'Abhishek@123'],
    ['Akshay', 'Akshay@123'],
    # Add more username-password pairs as needed
]

app = dash.Dash(__name__)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    dcc.Dropdown(id='x-axis-column'),
    dcc.Dropdown(id='y-axis-column'),
    dcc.Dropdown(
        id='visualization-type',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Plot', 'value': 'line'},
            {'label': 'Bar Plot', 'value': 'bar'}
        ],
        value='scatter'
    ),
    dcc.Graph(id='dynamic-graph')
])




def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode('utf-8')))

@app.callback(
    [Output('x-axis-column', 'options'),
     Output('y-axis-column', 'options')],
    [Input('upload-data', 'contents')]
)
def update_axis_options(contents):
    if contents is None:
        return [], []
    df = parse_contents(contents)
    options = [{'label': col, 'value': col} for col in df.columns]
    return options, options

@app.callback(
    Output('dynamic-graph', 'figure'),
    [Input('upload-data', 'contents'),
     Input('x-axis-column', 'value'),
     Input('y-axis-column', 'value'),
     Input('visualization-type', 'value')]
)
def update_graph(contents, x_column, y_column, visualization_type):
    if contents is None or not x_column or not y_column:
        return {}

    df = parse_contents(contents)

    if visualization_type == 'scatter':
        fig = px.scatter(df, x=x_column, y=y_column)
    elif visualization_type == 'line':
        fig = px.line(df, x=x_column, y=y_column)
    elif visualization_type == 'bar':
        fig = px.bar(df, x=x_column, y=y_column)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
