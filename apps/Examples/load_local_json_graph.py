# from apps.Examples.data_config import load_data_local
# import os
# import copy
# import time
# import datetime

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output, State
# import numpy as np
# import pandas as pd
# from datetime import date
# import plotly.graph_objs as go
# import plotly.express as px
# import plotly.io as pio

# from app import app, server, cache
# import utils

# available_files = os.listdir(utils.storage_dir)
# data = {}
# symbols = []
# frequencies = ["1D"]
# available_charts = []
# available_frequencies = []


# for fileName in available_files:
#     pretty_name = fileName[0:-4]
#     available_charts.append({'label':pretty_name,'value':fileName})

# chart_select_input = dbc.FormGroup(
#     [
#         dbc.Label("Select Chart", width=2),
#         dbc.Col(
#             dbc.Select(
#                 options=available_charts,
#                 value=[],
#                 id="chart_select_input",
#         ),
#         width=10,
#         )
#     ],
#     row=True,
# )

# layout = [
#     dcc.Store(id="store"),
#     dbc.Form([
#         chart_select_input,
#         ]), 
#     html.Br(),
#     dcc.Loading(id="chart_loading", children=[dcc.Graph(figure={}, id='loaded_chart_data')], type="default"),
# ]

# @app.callback(
#     Output(component_id='loaded_chart_data', component_property='figure'),
#     [Input('chart_select_input', "value")],
# )
# def load_config(config):
#     config = utils.load_local_json(config)
#     data = {}
#     for symbol in config['symbols']:
#         data[symbol] = utils.load_data_local(symbol)
#     # config = {
#     #     'start': start,
#     #     'end': end,
#     #     'title': name,
#     #     'symbols': list(data.keys()),
#     #     'hover_data':{
#     #         "time": "|%B %d, %Y"
#     #         },
#     #     'layout': {
#     #         'xaxis_title' : 'Date',
#     #         'yaxis_title' : 'f\'Scaled Close\'',
#     #         },
#     #     'xaxes': {
#     #         'value': "time",
#     #         'dtick':"M1",
#     #         'tickformat':"%b\n%Y",
#     #     },
#     #     'yaxes': {
#     #         'value': list(data.keys()),
#     #     },
#     #     # 'frequencies': frequencies,
#     #     # 'sample': sample,
#     # }
#     available_files = os.listdir(utils.storage_dir) 
#     if len(data.keys()) > 1:
#         df = utils.merge_timeseries(data, "scaled_close", "1H")[config['start']:config['end']]
#         print(df, config['title'], 'Complete. Sample Data above')
#         fig = px.line(df, x=config['xaxes']['value'], y=config['yaxes']['value'],
#             hover_data=config['hover_data'],
#             )
#         fig.update_layout(
#             title = config['title'],
#             xaxis_title = config['layout']['xaxis_title'],
#             yaxis_title = config['layout']['yaxis_title'],
#         )
#         fig.update_xaxes(
#             dtick=config['xaxes']['dtick'],
#             tickformat=config['xaxes']['tickformat'])
#         return fig
#     else:
#         print(data)
