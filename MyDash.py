# June 26 Chaoyi
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
#import ssl

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
    html.Label('Portfolio Optimizer'),
    #Hr() is a horizontal line
    html.Hr(),

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
            ], style={'width': '90%', 'float': 'left', 'display': 'inline-block','padding': '0 20'
                        , 'columns' : 2}
            ),
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

#selections appeared after user choose a optimization goal
#@app.callback(
#    Output(component_id ='subDiv', component_property='children'),
#    [Input(component_id='Optimization_Goal',component_property='value')]
#)
#def update_Goal_subDiv(input_value):
#    if input_value == 'Maximize Sharpe Ratio' :
#        return [html.Label('Start Month'),
#                dcc.Dropdown(options=[{'label': i, 'value' : i} for i in Compared_Allocation],value='None')]

if __name__ == '__main__':
    app.run_server(debug=True)
