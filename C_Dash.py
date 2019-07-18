#2019 July Chaoyi
import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True

# Dropdown choises specifying
years = ['1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995',
'1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007',
'2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

Optimization_Goal = ['Maximize Sharpe Ratio','Minimize Variance','Minimize Conditional Value-at-Risk',
'Risk Parity','Maximize Information Ratio','Minimize Volatility subject to...',
'Maximize Return subject to...','Minimize Maximum Drawdown subject to...',
'Maximize Omega Ratio subject to...','Maximize Sortino Ratio subject to...',
'Tail Risk Parity','Co-drawdown','Co-skew','Co-kurtosis','Resampling','Black-Litterman Allocation']

Compared_Allocation = ['None','Equal Weighted','Maximum Sharpe Ratio Weights',
'Inverse Volatility Weighted','Risk Parity Weighted']

#Number_Of_Assets = list(range(1,200))# is 200 enough?

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
        dcc.Dropdown(id='Optimization Goal',
            options=[{'label': i, 'value' : i} for i in Optimization_Goal],
            value='Maximize Sharpe Ratio'),
        html.Div(id='TAreturn'),
        #appear for everyone
        html.Label('Use Historical Returns'),
        dcc.RadioItems(id='HistoricalR',options=[{'label':'Yes','value':'Y'},
                                                    {'label':'No','value':'N'}],
                                            value = 'N',
                                            labelStyle={'display': 'inline-block'}),#label in one line
        html.Label('Asset Constraints'),
        dcc.RadioItems(id='AConstraints',options=[{'label':'Yes','value':'Y'},
                                                    {'label':'No','value':'N'}],
                                            value = 'N',
                                            labelStyle={'display': 'inline-block'}),#label in one line
        html.Label('Group Constraints'),
        dcc.RadioItems(id='GConstraints',options=[{'label':'Yes','value':'Y'},
                                                    {'label':'No','value':'N'}],
                                            value = 'N',
                                            labelStyle={'display': 'inline-block'}),#label in one line
        html.Label('Compared Allocation'),
        dcc.Dropdown(id='Compared Allocation',
            options=[{'label': i, 'value' : i} for i in Compared_Allocation],
            value='None'),
        #update later
        html.Div(id='BenchmarkDiv'),

            ],style={'width':'39%', 'display': 'inline-block'}
            ),
        html.Label('Portfolio Assets'),
        #give an example
        html.Div(html.A('(Download example format)', download='test.csv', href='/test.csv'),
                        style={'fontSize':'15px','float':'right'}),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Your Portfolio Files')
            ]),
            style={
                'width': '80%',
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

        #Or input Assets
        html.Label('OR Input Here'),
        #html.Div([html.Label('number of assets:'),
        #    dcc.Dropdown(id='NumberOfAssets',options=[{'label': i, 'value' : i} for i in Number_Of_Assets],
        #                value=0),
        #                ],style={'width':'20%','fontSize':'15px'}),
        html.Div(id='AssetsInput',children=[
            html.Label('Assets & Allocations'),
            dcc.Input(type='text'),dcc.Input(type='number')
            ],style={'width':'39%', 'display': 'inline-block','column':'2'}),
        #END
        html.Div([html.Button(id='submit_button', n_clicks=0, children='Submit',
        style={'background-color': '#045FB4','color':'white','float': 'right'})],
        ),
        html.Div([
            html.Hr(),
            html.H6('Optimization Results'),
            dcc.Tabs(id='tabs', value='1', children=[
            dcc.Tab(label='Summary', value='1'),
            dcc.Tab(label='Metrics', value='2'),
            dcc.Tab(label='Historical Returns', value='3'),
            dcc.Tab(label='Expected Returns', value='4')]
    ),
        html.Div(id='output-tab')
        ])
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
    Output('div3', 'children'),
    [Input('Period','value')]
)
def update_Period_div3(input_value):
    if input_value == 'MtM' :
        return [html.Label('End Month'),
                dcc.Dropdown(options=[{'label': i, 'value' : i} for i in months],value='Jan')]
@app.callback(
    Output('TAreturn', 'children'),
    [Input('Optimization Goal','value')]
)
def Targeted_Annual_Return(input_value):
    if ((input_value == 'Minimize Volatility subject to...') or (input_value == 'Maximize Return subject to...')
        or (input_value == 'Minimize Maximum Drawdown subject to...')
        or (input_value == 'Maximize Omega Ratio subject to...')
        or (input_value == 'Maximize Sortino Ratio subject to...')) :
            return [html.Label('Targeted Annual Return (%)'),
            dcc.Input(id='TAreturn',value = 10,type = 'number')] #has bugs!!only can input one time!!!

@app.callback(
    Output('BenchmarkDiv', 'children'),
    [Input('HistoricalR','value')]
)
def update_Benchmark(input_value):
    if input_value == 'Y' :
        return [html.Label('Benchmark'),
        dcc.Dropdown(id='Benchmark',options=[{'label':'Specify Ticker','value':'ST'},
                                                    {'label':'Import Benchmark','value':'Import'}],
                                            value = 'ST'),]

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
        )
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

#SUBMISSION(Get Results)
@app.callback(Output('output-tab', 'children'),
              [Input('submit_button', 'n_clicks'),
               Input('tabs','value')])
def update_tab(n_clicks,tabs):
    tickers = ['SPY', 'FB', 'AMZN']
    allocations = ['42344', '1864', '2390']
    column = ['Tickers','Allocations']

    if n_clicks >= 1:
        if tabs == '1':
            return html.Div([
                html.H6('Portfolio Allocations'),
                dash_table.DataTable(
                    id='result table',
                    data=allocations,
                    columns=[{'name': i, 'id': i} for i in column]
                ),
                dcc.Graph(id='tab1',
                           figure=go.Figure(
                               data=[go.Pie(labels=tickers,
                                            values=allocations)],
                               layout=go.Layout(
                                   title='Optimized weights')
                           ))
            ],style={})
        elif tabs == '2':
            return html.Div([
                html.H3('Tab content 2'),
                dash_table.DataTable(id='MetricsTable',data=['Arithmetic Mean','Volatility','Beta'],
                columns=['1','2'])
            ])

        elif tabs == '3':
            return html.Div([
                html.H3('Tab content 3'),
                dcc.Graph(
                    id='graph-3-tabs',
                    figure={
                        'data': [{
                            'x': [1, 2, 3],
                            'y': [5, 10, 6],
                            'type': 'scatter'
                        }]
                    }
                )
            ])



if __name__ == '__main__':
    app.run_server(debug=True)
