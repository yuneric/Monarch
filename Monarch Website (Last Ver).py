import dash
from dash.dependencies import Input, Output
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html

import datetime
#import pandas_datareader.data as web
import os

import pandas as pd
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import sys

import csv
            

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('M3 Monarch Migration Study'),

    dcc.Dropdown(['Duluth, MN', 'Gaylord, MI', 'Clinton, NY', 'Ypsilanti, MI',
                  'Kentwood, MI'],
                 id='location-dropdown',
                 placeholder = "Select a Location"),

    html.Br(),

    dcc.Dropdown(
    options={
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        },
        id='month-dropdown',
        placeholder = "Select a Month"),

    html.Br(),

    dcc.Dropdown(['Temperature', 'Light Intensity'],
                    id='templight-dropdown',
                    placeholder = "Plot Temperature or Light Intensity"),

    html.Div(id='dd-output-container'),

    html.Br(),


        
    #dcc.Input(id='input', value='', type='text'),
    
    #html.Br(),
    #html.Br(),
    #html.Button('Enter', id='submit-button'),
    
##    html.Div([
##    dcc.Graph(id='output-graph'),
##              figure = {
##                  'data': [
##                      {'x':time, 'y':temp, 'type':'line', 'name':'temp'},
##                      {'x':time, 'y':light, 'type':'line', 'name':'light'},
##                      ],
##                  'layout': {
##                      'title':'Basic Dash Example'
##                      }
##                })
##    ])

])

#@app.callback(
#    Output(component_id='output-graph', component_property='children'),
#    [Input(component_id='input', component_property='value')]
#    )

##@app.callback(
##    Output(component_id='dd-output-container', component_property='children'),
##    [Input(component_id='demo-dropdown', component_property='value')]
##    )

@app.callback(
    Output(component_id='dd-output-container', component_property='children'),
    [Input(component_id='location-dropdown', component_property='value'),
     Input(component_id='month-dropdown', component_property='value'),
     Input(component_id='templight-dropdown', component_property='value')]
    )
                      
#def update_output(value):
#   return f'You have selected {value}'    

def update_graph(location, month, templight):

    if location == 'Duluth, MN': sensorNum = '20433780'
    if location == 'Gaylord, MI': sensorNum = '20680275'
    if location == 'Clinton, NY': sensorNum = '20425153'
    if location == 'Ypsilanti, MI': sensorNum = '20680322'
    if location == 'Kentwood, MI': sensorNum = '20937747'

    mm = month
    date = '2021-' + mm #yyyy-mm-dd (ex: 2021-12-19)
    hobofilename = 'SN' + '_' + sensorNum + '_' + date

    path = "/Users/ericj/Exported CSV Files"
    #file = "/Users/Angela/Desktop/M3 Monarch Research/Data/Exported CSV Files/SN_20433780_2021-12-19_13_06_34_-0600_0.csv"
    with os.scandir(path) as it:
        for entry in it:
            if entry.name.startswith(hobofilename) and entry.is_file():
                file = path + "/" + entry.name


    #get csv file
    number = []
    time = []
    temp = []
    light = []

    with open(file,'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=(',' or ' '))
        line_count = 0
        for row in lines:
            if line_count == 0 or line_count == 1:
                line_count += 1
                continue
            else:
                number.append(row[0])
                time.append(row[1])
                temp.append(row[2])
                light.append(row[3])


        try:
##            fig = px.line(x=time, y=temp)
##            return fig
            if templight == 'Temperature':
                return    dcc.Graph(id='example',
                figure = {
                    'data': [
                        {'x':time, 'y':temp, 'type':'line', 'name':'temp'},
                        ],
                    'layout': {
                        'title': 'SN ' + sensorNum + ' / Month ' + mm + ' / ' + templight
                        }
                    })

            if templight == 'Light Intensity':
                return    dcc.Graph(id='example',
                figure = {
                    'data': [
                        {'x':time, 'y':light, 'type':'line', 'name':'light'},
                        ],
                    'layout': {
                        'title': 'SN ' + sensorNum + ' / Month ' + mm + ' / ' + templight
                        }
                    })
            
    
        except:
            return 'Error!'





if __name__ == '__main__':
    app.run_server(debug=True)
    


