import time
import json
import subprocess
from collections import deque

import dash
from dash import dcc, html, Input, Output, State, dash_table, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

from utils import log_example, asset_retrieving, transformation

# Cmd line for process
process = ["python", "json_generator.py"]

# Empty data for Table
table_data = pd.DataFrame(columns=['name', 'value'])

# Define the app state
state = {
    'data': deque(maxlen=10),
    'running': False,
    'paused': False
}

# Data for asset dropdown menu
ASSET_OPTIONS = asset_retrieving('asset.txt')

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

dash.register_page(__name__,
                   path='/realtime')

layout = html.Div([
    dbc.Row([
        # First graph
        dbc.Col(dcc.Graph(id='first-graph-realtime', ), width=5),

        dcc.Interval(
            id='interval-realtime',
            interval=1000,
            disabled=True),

        # Table
        dbc.Col([
            dash_table.DataTable(
                id='table-realtime',
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

    # Second graph
    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='second-graph-realtime', className='Spare-graph'), ], className='Spare-graph'),

        ], className='Spare-graph'),

        html.Div([
            # asset menu

            dcc.Dropdown(id='asset-realtime', className='mt-2', placeholder='Asset', options=ASSET_OPTIONS, value=None),

            # Add args input
            html.Button('Add Input', id='add-input-realtime', className='mt-2', n_clicks=0),
            html.Div(id='input-container-realtime', children=[], className='Inputs'),
        ], className=''),

    ], className='d-flex'),

    dbc.Row([
        dbc.Col(dbc.Button('Start', id='start-button-realtime',
                           n_clicks=0, disabled=False,
                           active=False, outline=True,
                           style={'background-color': "#c32aff"}), width=1),
        dbc.Col(dbc.Button('Pause', id='pause-button-realtime', n_clicks=0,
                           disabled=True, outline=True,
                           style={'background-color': "#c32aff"}), width=1),
        dbc.Col(dbc.Button('Reset', id='reset-button-realtime', n_clicks=0,
                           disabled=True, outline=True,
                           style={'background-color': "#c32aff"})),
    ]),

], style={'margin-left': '80px',
          'margin-right': '80px',
          'margin-top': '20px',
          })


@callback(
    Output('start-button-realtime', 'disabled'),
    Output('pause-button-realtime', 'disabled'),
    Output('reset-button-realtime', 'disabled'),
    Output('interval-realtime', 'disabled'),
    Output('start-button-realtime', 'n_clicks'),
    Output('pause-button-realtime', 'n_clicks'),
    Output('reset-button-realtime', 'n_clicks'),

    Output('asset-realtime', 'value'),
    Output('input-container-realtime', 'children'),
    Output('add-input-realtime', 'n_clicks'),

    Input('start-button-realtime', 'n_clicks'),
    Input('pause-button-realtime', 'n_clicks'),
    Input('reset-button-realtime', 'n_clicks'),
    Input('add-input-realtime', 'n_clicks'),

    State('start-button-realtime', 'disabled'),
    State('pause-button-realtime', 'disabled'),
    State('reset-button-realtime', 'disabled'),
    State('interval-realtime', 'disabled'),

    State('asset-realtime', 'value'),
    State('input-container-realtime', 'children'))
def update_state(start_clicks: int, pause_clicks: int, reset_clicks: int, add_input_clicks: int,
                 start_disabled: bool, pause_disabled: bool, reset_disabled: bool, interval_disabled: bool,
                 asset: str, children: list):
    """
        Make interactions with UI when one of the buttons are pressed.
        When 'Start' button is pressed, new process starts. If 'Stop' or 'Reset' current process terminates. Also,
        with pressing 'Reset' all data, inputs become empty.

        Args:
            start_clicks (int): sum how many times start_button was clicked
            pause_clicks (int): sum how many times pause_clicks was clicked
            reset_clicks (int): sum how many times reset_clicks was clicked
            add_input_clicks (int): sum how many times add_input_clicks was clicked
            start_disabled (bool): start_button state(enabled or disabled)
            pause_disabled (bool): pause_disabled state(enabled or disabled)
            reset_disabled (bool): reset_disabled state(enabled or disabled)
            interval_disabled (bool): interval_disabled state(enabled or disabled)
            asset (str): asset option or empty string
            children (list): inputs or []
        Returns:
             Tuple[int, int, int, int, bool, bool, bool, bool, str, list]: start_disabled, pause_disabled,
              reset_disabled, interval_disabled, start_clicks, pause_clicks, reset_clicks, asset, children,
              add_input_clicks
    """

    # Args parsing
    if add_input_clicks > 0:
        name_input = dcc.Input(
            id={'type': 'dynamic-input', 'index': add_input_clicks},
            type='text',
            placeholder='arg name'
        )
        value_input = dcc.Input(
            id={'type': 'dynamic-input', 'index': add_input_clicks},
            # type='number',
            placeholder='value'
        )
        children.append(name_input)
        children.append(value_input)
        add_input_clicks = 0

    if asset:
        process.append('-a')
        process.append(asset)

    # Handle start button click
    if start_clicks > 0:
        state['running'] = True
        state['paused'] = False
        start_disabled = True
        pause_disabled = False
        reset_disabled = False
        interval_disabled = False
        start_clicks = 0

        inputs = [child['props']['value'] for child in children]

        for _ in inputs:
            option = transformation(_)
            process.append(option)

        # Start data_generator for Windows
        # subprocess.Popen(process, shell=True)

        # Start data_generator for Amazon linux
        subprocess.Popen(process)
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
        with open('pid.txt', 'r') as file:
            process_id = file.readline()

        # Start data_generator for Windows
        # subprocess.call(["taskkill", "/PID", process_id, '/F'], shell=True)

        # Start data_generator for Amazon linux
        subprocess.run(f"kill {process_id}", shell=True)

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
        start_date, end_date, asset = None, None, None
        time.sleep(1)
        children = []

        # Terminate data_generator
        with open('pid.txt', 'r') as file:
            process_id = file.readline()

        # Start data_generator for Windows
        # subprocess.call(["taskkill", "/PID", process_id, '/F'], shell=True)

        # Start data_generator for Amazon linux
        subprocess.run(f"kill {process_id}", shell=True)

        # Write empty data
        with open('data.json', 'w') as f:
            data = log_example()
            json.dump(data, f, indent=4)

        print('reset')
        print('-----------------------------------')

    return (start_disabled, pause_disabled, reset_disabled, interval_disabled, start_clicks, pause_clicks, reset_clicks,
            asset, children, add_input_clicks)


@callback(
    Output('first-graph-realtime', 'figure'),
    Output('second-graph-realtime', 'figure'),
    Output('table-realtime', 'data'),

    Input('interval-realtime', 'n_intervals'),
    Input('start-button-realtime', 'n_clicks')
)
def update_graph_scatter(n1: int, start_button_clicks: int):
    """
        Returns two graphs and table. When no data, returns empty graphs, table and prints string 'No data.
        Updates every interval value.

        Args:
            n1 (int): interval value
            start_button_clicks (int): sum how many times start_button was clicked
        Returns:
            if No Data:
                Tuple[px.line, px.line, pd.Dataframe]: fig, fig, table_data.to_dict('records')
            if Data:
                Tuple[px.line, px.line, pd.Dataframe]: fig1, fig2, df_for_table.to_dict('records')
    '"""

    fig = px.line()
    try:
        # Data for components
        with open('data.json', 'r') as f:
            data = json.load(f)

        df_for_fig1 = pd.DataFrame(data['charts'][0])
        df_for_fig2 = pd.DataFrame(data['charts'][1])

        # table = table_data.append(df_for_table, ignore_index=True)
        df_for_table = pd.DataFrame(columns=['name', 'value'],
                                    data=[[i, data['markers_table'][i][0]] for i in data['markers_table']])

        # Firs graph
        fig1 = px.line(df_for_fig1, x=df_for_fig1['timestamp'], y=df_for_fig1['portfolio_value'], markers=True, )
        fig1.update_traces(line_color='#E450FF')
        fig1.update_layout(template=CHARTS_TEMPlATE)

        # Second graph
        fig2 = px.line(df_for_fig2, x=df_for_fig2['timestamp'], y=df_for_fig2['price'], markers=True, )
        fig2.update_traces(line_color='#E450FF')
        fig2.update_layout(template=CHARTS_TEMPlATE)
        return fig1, fig2, df_for_table.to_dict('records')

    except Exception:
        print('no data')
        fig.update_layout(template=CHARTS_TEMPlATE)
        return fig, fig, table_data.to_dict('records')
