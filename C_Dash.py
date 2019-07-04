#July 4th Chaoyi
import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Dropdown choises specifying
years = ['1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995',
'1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007',
'2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

Optimization_Goal = ['Maximize Sharpe Ratio','Minimize Volatility subject to...',
'Minimize Volatility subject to...','Maximize Return subject to...','Minimize Variance',
'Minimize Conditional Value-at-Risk','Risk Parity','Maximize Information Ratio',
'Minimize Maximum Drawdown subject to...','Maximize Omega Ratio subject to...',
'Maximize Sortino Ratio subject to...']

Compared_Allocation = ['None','Equal Weighted','Maximum Sharpe Ratio Weights',
'Inverse Volatility Weighted','Risk Parity Weighted']


app.layout = html.Div([
    html.Div([html.Label('Portfolio Optimizer'),
    #Hr() is a horizontal line
    html.Hr()],style={'color':'#045FB4','fontSize' : '30px'}),

    html.Div(className = 'Selections',children=[

        html.Label('Time Period'),
        dcc.Dropdown(
            id = 'Period',
            options=[
            {'label':'Month-to-Month','value':'MtM'},
            {'label':'Year-to-Year','value':'YtY'}
            ],
            value='YtY'
            ),
        html.Label('Start Year'),
            dcc.Dropdown(
            id = 'Start-year',
            options=[{'label': i, 'value' : i} for i in years],
            value='2018'
            ),
            html.Div(id = 'div2'),
            html.Label('End Year'),
            dcc.Dropdown(
            id = 'End-year',
            options=[{'label': i, 'value' : i} for i in years],
            value='2018'
            ),
            html.Div(id = 'div3'),
        html.Label('Portfolio Type'),
        dcc.Dropdown(
            id = 'Type',
            options=[
                {'label':'Asset Classes','value':'AC'},
                {'label':'Tickers','value':'T'}
            ], value='T'),

        #html.Hr(),
        html.Label('Optimization Goal'),
        dcc.Dropdown(id='Goal',
            options=[{'label': i, 'value' : i} for i in Optimization_Goal],
            value='Maximize Sharpe Ratio'),
        #update later
        html.Div(id='subDiv'),
        #appear for everyone
        html.Label('Asset Constraints'),
        dcc.Dropdown(id='AConstraints',options=[{'label':'Yes','value':'Y'},
                                                    {'label':'No','value':'N'}],
                                            value = 'N'),
        html.Label('Compared Allocation'),
        dcc.Dropdown(id='Compared Allocation',
            options=[{'label': i, 'value' : i} for i in Compared_Allocation],
            value='None'),
        html.Label('Benchmark'),
        dcc.Dropdown(id='Benchmark',options=[{'label':'Specify Ticker','value':'ST'},
                                                    {'label':'Import Benchmark','value':'Import'}],
                                            value = 'ST'),
            ],style={'width':'39%'}
            ),

        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Your Portfolio Files')
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
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-data-upload'),
])

@app.callback(
    Output(component_id ='div2', component_property='children'),
    [Input(component_id='Period',component_property='value')]
)
def update_Period_div2(input_value):
    if input_value == 'MtM' :
        return [html.Label('Start Month'),
                dcc.Dropdown(options=[{'label': i, 'value' : i} for i in months],value='Jan')]

@app.callback(
    Output(component_id ='div3', component_property='children'),
    [Input(component_id='Period',component_property='value')]
)
def update_Period_div3(input_value):
    if input_value == 'MtM' :
        return [html.Label('End Month'),
                dcc.Dropdown(options=[{'label': i, 'value' : i} for i in months],value='Jan')]

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



if __name__ == '__main__':
    app.run_server(debug=True)
