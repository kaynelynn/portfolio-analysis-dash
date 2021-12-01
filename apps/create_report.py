from datetime import datetime
import os
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_table
import pystore
import talib as ta
from app import app
from apps.utils.component_factory import create_text_input, create_date_input, create_checklist_input, create_dropdown_input
from apps.utils.local_storage import LocalStorage
import utils 
import ffn
import IPython

storage_dir = '/Volumes/CAPA/.storage'
data = {}
chart_data = {}
pystore.set_path(storage_dir)
store = pystore.store('capa_store')
collection = store.collection('Crypto.Candles')
collections = store.list_collections()
items = collection.list_items()
available_symbols = items
# storage = LocalStorage()
# available_files = storage.available_files
data = {}

all_symbols = [

]
for s in available_symbols:
    all_symbols.append(s + "/Day")
my_symbols = [
    "ETH/Day",
    "BTC/Day",
    # "MATIC/Day",
    # "CRO/Day",
    # "FIL/Day",
    # "UNI/Day",
    # "BAT/Day",
    # "LINK/Day",
    # "GRT/Day",
    # "AAVE/Day",
    # "COMP/Day",
    # "SNX/Day"
    ]
symbols =[]
frequencies = ["1D"]
available_frequencies = []

# available_frequencies_raw = {
#     'B':'business day frequency',
#     'C':'custom business day frequency',
#     'D':'calendar day frequency',
#     'W':'weekly frequency',
#     'M':'month end frequency',
#     'SM':'semi-month end frequency (15th and end of month)',
#     'BM':'business month end frequency',
#     'CBM':'custom business month end frequency',
#     'MS':'month start frequency',
#     'SMS':'semi-month start frequency (1st and 15th)',
#     'BMS':'business month start frequency',
#     'CBMS':'custom business month start frequency',
#     'Q':'quarter end frequency',
#     'BQ':'business quarter end frequency',
#     'QS':'quarter start frequency',
#     'BQS':'business quarter start frequency',
#     'Y ':'year end frequency',
#     'BY':'business year end frequency',
#     'YS':'year start frequency',
#     'BYS':'business year start frequency',
#     'BH':'business hour frequency',
#     'H':'hourly frequency',
#     'min':'minutely frequency',
#     'S':'secondly frequency',
#     'ms':'milliseconds',
#     'us':'microseconds',
#     'N':'nanoseconds',
# }
indicators = [
    {'label': 'Close', 
    'value':'close'},
    {'label': 'Scaled Close',
    'value':'scaled_close'},    
    # {'label': 'Rebase',
    # 'value':'rebase'},
    {'label': 'Volume',
    'value':'volume'},
    {'label': '30 Day SMA - Close',
    'value':'sma_30_close'},
    {'label': '60 Day SMA - Close',
    'value':'sma_60_close'},
    {'label': '90 Day SMA - Close',
    'value':'sma_90_close'},
    {'label': '30 Day SMA - Scaled Close',
    'value':'sma_30_scaled_close'},
    {'label': '60 Day SMA - Scaled Close',
    'value':'sma_60_scaled_close'},
    {'label': '90 Day SMA - Scaled Close',
    'value':'sma_90_scaled_close'},
]

for available_symbol in available_symbols:
    symbols.append({'label':available_symbol,'value':available_symbol + "/Day"})
# title
report_name_input = create_text_input("Report Name", "report_name_input", "2015-2016 MegaCap Minutely")

# date range
report_start_input = create_date_input("Analysis Start Date", "report_start_input", "Select a start date.","2020-01-01")
report_end_input = create_date_input("Analysis End Date", "report_end_input", "Select a end date.","2021-05-01")

# symbols
report_symbols_input = create_checklist_input("Select Assets to Include", "report_symbols_input", initial=all_symbols, options=sorted(symbols, key = lambda i: i['label']))
report_indicator_input = create_dropdown_input("Select Indicator", 'report_indicator_input',initial='scaled_close',
options=indicators)
generate_report_button = dbc.Button("Update Graph", color="primary", id="generate_report_button", outline=True, block=True)
save_chart_button = dbc.Button("Save Report", color="primary", id="save_chart_button", outline=True, block=True)
# columns=[{"symbol": i, "id": i} for i in correlations]
layout = [
    dcc.Store(id="store"),
    dbc.Form([
        report_name_input,
        report_start_input, 
        report_end_input, 
        report_symbols_input,
        report_indicator_input,
        html.Div([html.Br(), save_chart_button], id="submit_button_row")]),
        html.Div([html.Br(), generate_report_button], id="submit_button_row"),
    html.Br(),
    html.Div(id='symbol_list'),
    html.Div(id='indicator_list'),
    html.Div(id='save_report'),
    html.Div(id='date_range'),
    dcc.Loading(id="chart_loading", children=[dcc.Graph(figure={}, id='chart_data')], type="default"),
]

@app.callback(
    Output(component_id='chart_data', component_property='figure'),
    [Input('generate_report_button', "n_clicks")],
    State('report_start_input', 'value'),
    State('report_end_input', 'value'),
    State('report_name_input', 'value'),
    State('report_indicator_input', 'value'),
) 
def generate_chart(n, start, end, name, ind):
    if len(data.keys()) > 1:
        df = utils.merge_timeseries(data, ind, "1D")[start:end]
        # print(df, name, 'Complete. Sample Data above')
        fig = px.line(df, x="time", y=df.columns,
              hover_data={"time": "|%B %d, %Y"},
              )
        fig.update_layout(
            title = name,
            xaxis_title = 'Date',
            yaxis_title = ind,
        )
        fig.update_xaxes(
            dtick="M1",
            tickformat="%b\n%Y")
        # print(df.columns)
        return fig
    else:
        return {}


@app.callback(
    Output(component_id='save_report', component_property='value'),
    [Input('save_chart_button', "n_clicks")],
    State('report_start_input', 'value'),
    State('report_end_input', 'value'),
    State('report_name_input', 'value'),
)
def save_config(n, start, end, name):
    config = {
        'start': start,
        'end': end,
        'title': name,
        'symbols': list(data.keys()),
        'hover_data':{
            "time": "|%B %d, %Y"
            },
        'layout': {
            'xaxis_title' : 'Date',
            'yaxis_title' : 'f\'Scaled Close\'',
            },
        'xaxes': {
            'value': "time",
            'dtick':"M1",
            'tickformat':"%b\n%Y",
        },
        'yaxes': {
            'value': list(data.keys()),
        },
    }
    # if name:
        # storage.save_json(config, name)
    return name

@app.callback(
    Output(component_id='symbol_list', component_property='value'),
    Input(component_id='report_symbols_input', component_property='value')
)
def update_symbols(input_value):
    for symbol in input_value:
        data[symbol] = collection.item(symbol).to_pandas()
        utils.scaled_close(data[symbol])

    return input_value

@app.callback(
    Output(component_id='indicator_list', component_property='value'),
    Input(component_id='report_indicator_input', component_property='value'),
    State('report_start_input', 'value'),
    State('report_end_input', 'value'),
)
def update_indicators(input_value, start, end):
    for sym in data:
        utils.scaled_close(data[sym])
        close_array = data[sym]['close'].to_numpy()
        scaled_array = data[sym]['scaled_close'].to_numpy()
        # if input_value == 'rebase':
        #     data[sym][input_value] = ffn.rebase(data[sym][start:end], 1)
        if input_value == 'sma_30_close':
            data[sym][input_value] = ta.SMA(close_array,30)
        elif input_value == 'sma_60_close':
            data[sym][input_value] = ta.SMA(close_array,60)
        elif input_value == 'sma_90_close':
            data[sym][input_value] = ta.SMA(close_array,90)
        elif input_value == 'sma_30_scaled_close':
            data[sym][input_value] = ta.SMA(scaled_array,30)
        elif input_value == 'sma_60_scaled_close':
            data[sym][input_value] = ta.SMA(scaled_array,60)
        elif input_value == 'sma_90_scaled_close':
            data[sym][input_value] = ta.SMA(scaled_array,90)
    return input_value

@app.callback(
    Output(component_id='report_name_output', component_property='children'),
    Input(component_id='report_name_input', component_property='value')
)
def update_name(input_value):
    return input_value

@app.callback(
    Output('date_range', 'children'),
    [Input('date_range_picker', 'report_start_input'),
    Input('date_range_picker', 'report_end_input')])
def update_date_range(start_date, end_date):
    for symbol in data.keys():
        data[symbol] = data[symbol][start_date:end_date]
    return start_date, end_date
