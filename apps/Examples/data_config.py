import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
from datetime import date
from app import app



data_dir = os.path.abspath(os.path.curdir) + "/data/minute"
available_files = os.listdir(data_dir)
data = {}
symbols = []
frequencies = ["1H"]
available_symbols = []
available_frequencies = []

available_frequencies_raw = {
'B':'business day frequency',
'C':'custom business day frequency',
'D':'calendar day frequency',
'W':'weekly frequency',
'M':'month end frequency',
'SM':'semi-month end frequency (15th and end of month)',
'BM':'business month end frequency',
'CBM':'custom business month end frequency',
'MS':'month start frequency',
'SMS':'semi-month start frequency (1st and 15th)',
'BMS':'business month start frequency',
'CBMS':'custom business month start frequency',
'Q':'quarter end frequency',
'BQ':'business quarter end frequency',
'QS':'quarter start frequency',
'BQS':'business quarter start frequency',
'A, Y ':'year end frequency',
'BA, BY':'business year end frequency',
'AS, YS':'year start frequency',
'BAS, BYS':'business year start frequency',
'BH':'business hour frequency',
'H':'hourly frequency',
'min':'minutely frequency',
'S':'secondly frequency',
'L, ms':'milliseconds',
'U, us':'microseconds',
'N':'nanoseconds',
}


for fileName in available_files:
    if fileName.endswith("usd.csv"):
        name = fileName[0:-7]
        available_symbols.append({'label':name,'value':name})

for frequency in available_frequencies_raw:
    available_frequencies.append({'label':available_frequencies_raw[frequency],'value':frequency})


symbol_selector = dcc.Checklist(
    id='symbol_checklist',
    options=available_symbols,
    value=['btc'])

frequency_dropdown = dcc.Dropdown(
    id='frequency_dropdown',
    options=available_frequencies,
)

frequency_interval = dcc.Input(
    id='frequency_interval',
    type="number",
    value=1)

add_frequency_button = html.Button(
    "Add Frequency", 
    id="add_frequency")

date_picker = dcc.DatePickerRange(
        id='date_range_picker',
        min_date_allowed=date(2010, 1, 1),
        max_date_allowed=date.today(),
        initial_visible_month=date(2015, 1, 1),
        end_date=date.today()
    )

layout = html.Div([
    html.Div(["Select Date Range: ", date_picker]),
    html.Br(),
    html.Div(id="selected_symbols"),
    html.Br(),
    html.Div(["Select Symbols: ",
              symbol_selector]),    
    html.Br(),
    html.Div(["Select Frequency: ",frequency_dropdown]),
    html.Br(),
    html.Div(["Select Insterval: ",frequency_interval]),
    html.Br(),
    add_frequency_button,
    html.Br(),
])


def load_data_local(symbol):
    df = pd.read_csv('/Users/kaynelynn/Dev/CAPA-DASH/data/minute/'+symbol+'usd.csv', parse_dates=True)
    df['time'] = pd.to_datetime(df["time"], unit="ms")
    df.set_index('time',drop=False, inplace=True)
    df['symbol'] = symbol
    if "Unnamed: 0" in df.columns:
        del df["Unnamed: 0"]
    data[symbol] = df

@app.callback(
    Output(component_id='selected_symbols', component_property='children'),
    Input(component_id='symbol_checklist', component_property='value')
)
def update_symbols(input_value):
    symbols = (input_value)
    for symbol in symbols:
        if symbol not in data:
            load_data_local(symbol)
    return "Data loaded for: " + ", ".join(data.keys())

@app.callback(
    dash.dependencies.Output('added_frequencies', 'children'),
    [dash.dependencies.Input('add_frequency', 'n_clicks')],
    [dash.dependencies.State('frequency_interval', 'value')],
    [dash.dependencies.State('frequency_dropdown', 'value')])
def add_frequency(n_clicks, value1, value2):
    if value1 and value2 :
        frequencies.append(str(value1) + str(value2[0]))
    return ", ".join(frequencies)


@app.callback(
    dash.dependencies.Output('current_date_range', 'children'),
    [dash.dependencies.Input('date_range_picker', 'start_date'),
     dash.dependencies.Input('date_range_picker', 'end_date')])
def update_date_range(start_date, end_date):
    string_prefix = ""
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + start_date_string + ' - '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + end_date_string
    return string_prefix

if __name__ == '__main__':
    app.run_server(debug=True)









# for frequency in current_frequencies:
#     for dataset in data:
#         change_percent(frequency, data[dataset])
#         change_log(frequency, data[dataset])
#         change_usd(frequency, data[dataset])
#         scaled_close(data[dataset])
# print(asset_statistics(data, frequency))