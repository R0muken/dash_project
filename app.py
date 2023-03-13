from dash import Dash, dcc, html, Input, Output, State, dash_table

import plotly
import plotly.express as px
import plotly.graph_objs as go

import pandas as pd

from collections import deque, OrderedDict

import subprocess
import random
import time
import json
import dash_bootstrap_components as dbc

from json_generator import log_example

# Empty data for Table
table_data = pd.DataFrame(columns=['name', 'value'])

# Define the app state
state = {
    'data': deque(maxlen=10),
    'running': False,
    'paused': False
}

# GLOBAL DESIGN SETTINGS
CHARTS_TEMPlATE = go.layout.Template(
    layout=dict(
        font=dict(
            color='white',
        ),
        plot_bgcolor='#440060',
        paper_bgcolor='#440060',
        # xaxis=dict(gridcolor="#CCCCCC"),
        yaxis=dict(gridcolor="#CCCCCC"),
    )
)

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Graph(id='main-graph', ), width=5),
        dcc.Interval(
            id='interval',
            interval=1000,
            disabled=True),
        dbc.Col([
            dash_table.DataTable(
                id='table',
                columns=[{'name': i, 'id': i} for i in table_data.columns],
                data=table_data.to_dict('records'),
                page_size=9,


                style_table={'maxWidth': '800px', 'maxHeight': '400px'},
                style_header={
                    'backgroundColor': '#440060',
                    'color': '#BA25F9'
                },
                style_data={
                    'backgroundColor': '#5E0086',
                    'color': 'white'
                })

        ]),
    ]),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='spare-graph', className='Spare-graph'), ], className='Spare-graph'),

        ], className='Spare-graph'),

        html.Div([
            dcc.Dropdown(placeholder='Date1', className='mb-2'),
            dcc.Dropdown(placeholder='Date1', className='mb-2'),
            dcc.Dropdown(placeholder='Asset'),
        ], className='w-25'),

    ], className='d-flex'),

    dbc.Row([
        dbc.Col(dbc.Button('Start', id='start-button',
                           n_clicks=0, disabled=False,
                           active=False, outline=True,
                           style={'background-color': "#c32aff"}), width=1),
        dbc.Col(dbc.Button('Pause', id='pause-button', n_clicks=0,
                           disabled=True, outline=True,
                           style={'background-color': "#c32aff"}), width=1),
        dbc.Col(dbc.Button('Reset', id='reset-button', n_clicks=0,
                           disabled=True, outline=True,
                           style={'background-color': "#c32aff"})),
    ]),

], style={'margin-left': '80px',
          'margin-right': '80px',
          'margin-top': '20px',
          })


# CALLBACK FOR BUTTONS
@app.callback(
    Output('start-button', 'disabled'),
    Output('pause-button', 'disabled'),
    Output('reset-button', 'disabled'),
    Output('interval', 'disabled'),
    Output('start-button', 'n_clicks'),
    Output('pause-button', 'n_clicks'),
    Output('reset-button', 'n_clicks'),

    Input('start-button', 'n_clicks'),
    Input('pause-button', 'n_clicks'),
    Input('reset-button', 'n_clicks'),

    State('start-button', 'disabled'),
    State('pause-button', 'disabled'),
    State('reset-button', 'disabled'),
    State('interval', 'disabled'))
def update_state(start_clicks, pause_clicks, reset_clicks, start_disabled, pause_disabled, reset_disabled,
                 interval_disabled):
    # Handle start button click
    if start_clicks > 0:
        state['running'] = True
        state['paused'] = False
        start_disabled = True
        pause_disabled = False
        reset_disabled = False
        interval_disabled = False
        start_clicks = 0

        # Start data_generator
        subprocess.Popen(["python", "json_generator.py"], shell=True)
        print('start')

    # Handle pause button click
    if pause_clicks > 0 and state['running']:
        state['paused'] = not state['paused']
        pause_disabled = True if state['paused'] else False
        start_disabled = False
        interval_disabled = True
        pause_clicks = 0

        time.sleep(1)

        # Terminate data_generator
        file = open('pid.txt', 'r')
        process_id = file.readline()
        subprocess.call(["taskkill", "/PID", process_id, '/F'], shell=True)
        print('stop')

    # Handle reset button click
    if reset_clicks > 0:
        state['running'] = False
        state['paused'] = False
        start_disabled = False
        pause_disabled = True
        reset_disabled = True
        interval_disabled = True
        start_clicks = 0
        pause_clicks = 0
        reset_clicks = 0

        time.sleep(1)

        # Terminate data_generator
        file = open('pid.txt', 'r')
        process_id = file.readline()
        subprocess.call(["taskkill", "/PID", process_id, '/F'], shell=True)

        # Write empty data
        with open('data.json', 'w') as f:
            data = log_example()
            json_data = json.dumps(data, indent=4)
            f.write(json_data)
        print('reset')

    return start_disabled, pause_disabled, reset_disabled, interval_disabled, start_clicks, pause_clicks, reset_clicks


@app.callback(
    Output('main-graph', 'figure'),
    Output('spare-graph', 'figure'),
    Output('table', 'data'),
    Input('interval', 'n_intervals'),
    Input('start-button', 'n_clicks')
)
def update_graph_scatter(n1, start_button_clicks):
    global table_data

    fig = px.line()
    try:
        # Data for components
        data = json.load(open('data.json'))
        df_for_fig1 = pd.DataFrame(data['charts'][0])
        df_for_fig2 = pd.DataFrame(data['charts'][1])
        # df_for_table = pd.DataFrame(data['markers_table'])

        # table = table_data.append(df_for_table, ignore_index=True)
        table = table_data.append(pd.DataFrame([[i, data['markers_table'][i]] for i in data['markers_table']]), ignore_index=True)
        c = pd.DataFrame(data=table)


        # Firs graph
        fig1 = px.line(df_for_fig1, x=df_for_fig1['timestamp'], y=df_for_fig1['portfolio_value'], markers=True, )
        fig1.update_traces(line_color='#E450FF')
        fig1.update_layout(template=CHARTS_TEMPlATE)

        # Second graph
        fig2 = px.line(df_for_fig2, x=df_for_fig2['timestamp'], y=df_for_fig2['price'], markers=True, )
        fig2.update_traces(line_color='#E450FF')
        fig2.update_layout(template=CHARTS_TEMPlATE)
        return fig1, fig2, table.to_dict('records')

    except:
        print('no data')
        fig.update_layout(template=CHARTS_TEMPlATE)
        return fig, fig, table_data.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
