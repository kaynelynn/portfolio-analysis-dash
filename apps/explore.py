import json
from utils import merge_timeseries
from apps.utils.component_factory import create_card_list
from apps.utils.local_storage import LocalStorage
from apps.utils.charts import generate_chart
import os

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, MATCH
from app import app
import dash



storage = LocalStorage()
saved = os.listdir(storage.storage_dir)
saved_charts = []
for fileName in saved:
    pretty_name = fileName[0:-4]
    saved_charts.append({'label':pretty_name,'value':fileName}) 
list = create_card_list(saved_charts)

layout = [html.Div(list)
]

@app.callback(
    Output({'type': 'current_figure', 'index': MATCH}, component_property='figure'),
    Input({'type': 'load_graph_button', 'index': MATCH}, "n_clicks"),
    State({'type': 'load_graph_button', 'index': MATCH}, 'id'),
    prevent_initial_call=True
)
# @cache.memoize(timeout=3600)  # in seconds
def viewchart(n, id):
    config = storage.load_json(id['index'])
    # config = utils.load_local_json(config)
    data = {}
    for symbol in config['symbols']:
        data[symbol] = storage.load_csv(symbol)
    fig = generate_chart(config['title'], data,"close", config['hover_data'], config['layout'],{
            'value': config['symbols'],
        },{'value': "time",
            'dtick':"M1",
            'tickformat':"%b\n%Y",
        },)
    return fig