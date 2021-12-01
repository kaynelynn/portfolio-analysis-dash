from datetime import datetime
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pandas.core.algorithms import SelectNFrame
import pystore
import utils
from app import app
from apps.utils.component_factory import create_text_input, create_date_input, create_checklist_input, create_dropdown_input
import bt
import pandas as pd
import ffn
import urllib
import json
storage_dir = '/Volumes/CAPA/.storage'
all_symbols = []
all_symbols_input =[]
saved_symbol_groups = utils.load_local_json('Symbols')
saved_symbol_groups_input =[]
saved_dates = utils.load_local_json('Dates')
saved_dates_input =[]
saved_backtests = utils.load_local_json('Strategies')
saved_backtests_input =[]
pystore.set_path(storage_dir)
store = pystore.store('historical')
db_store = pystore.store('local_storage')
collections = store.list_collections()
collection = store.collection('Crypto.Candles')
items = collection.list_items()

for s in items:
    all_symbols.append(s)

for available_symbol in all_symbols:
    all_symbols_input.append({'label':available_symbol,'value':available_symbol})

for sym in saved_symbol_groups: 
    saved_symbol_groups_input.append({
        'label' : sym,
        'value' : sym
    })
for dat in saved_dates: 
    saved_dates_input.append({
        'label' : dat,
        'value' : dat
    })
for backt in saved_backtests: 
    saved_backtests_input.append({
        'label' : backt,
        'value' : backt
    }) 

symbol_data_frequencies = [
    {'label' : 'Day',
    'value' :  '/Day',},
    {'label' : 'Minute',
    'value' : '/Min'}
]

strategy_frequencies = [
    {'label' : 'Once',
    'value' :  'once',},
    {'label' : 'Weekly',
    'value' :  'weekly',},
    {'label' : 'Monthly',
    'value' :  'monthly'},
    {'label' : 'Quarterly',
    'value' :  'quarterly'},
    {'label' : 'Yearly',
    'value' :  'yearly'},
]

strategy_weightings = [
    {'label' : 'Equal',
    'value' :  'equal'},
    {'label' : 'Inverse Variance',
    'value' :  'inv-var'},
    {'label' : 'Mean Variance',
    'value' :  'mean-var'},
    {'label' : 'ERC',
    'value' :  'erc'},
]


backtest_name = create_text_input("Name", "backtest_name", None, initial="Default")
save_symbol_name = create_text_input("Name", "save_symbol_name", None, initial="Default")
save_strategy_name = create_text_input("Name", "save_strategy_name", None, initial="Default")

load_symbols_dropdown = create_dropdown_input("Symbols", 'load_symbols_dropdown',initial='Default', options=saved_symbol_groups_input)
load_strategies_dropdown = create_dropdown_input("Strategies", 'load_strategies_dropdown',initial='Default',  options=saved_backtests_input)
save_backtest_button = dbc.Button("Save", color="primary", id="save_backtest_button", block=True)
new_symbols_button = dbc.Button("+", color="primary", id="new_symbols_button", block=True)
new_strategy_button = dbc.Button("+", color="primary", id="new_strategy_button", block=True)
new_symbols_button_dropdown = create_dropdown_input("Select symbols", 'new_symbols_button_dropdown', options=sorted(all_symbols_input, key = lambda i: i['label']), multi=True)
new_start_input = create_date_input("Start Date", "new_start_input", "Select a start date.","2018-01-01")
new_end_input = create_date_input("End Date", "new_end_input", "Select an end date.","2021-06-01")

new_frequncy_input = create_dropdown_input("Frequency", 'new_frequncy_input', initial='weekly', options=strategy_frequencies)
new_weighting_input = create_dropdown_input("Weighting", 'new_weighting_input', initial='equal',  options=strategy_weightings)
new_data_freq_input = create_dropdown_input("Data Freq", 'new_data_freq_input', initial='/Day',  options=symbol_data_frequencies)

symbol_modal = html.Div(
    [
        dbc.Modal([
                dbc.ModalHeader("New Symbol Group"),
                dbc.ModalBody([
                    dbc.Col([
                        dbc.Row(dbc.Col(save_symbol_name)),
                        dbc.Row([
                            dbc.Col(new_symbols_button_dropdown),
                        ]),
                        dbc.Row([
                            dbc.Col(new_data_freq_input),
                        ]),        
                    ])
                ]),
                dbc.ModalFooter(
                    dbc.Button("Save", id="save_symbol", className="ml-auto")
                ),
            ],
            id="symbol_modal",
        ),
    ]
)

strategy_modal = html.Div(
    [
        dbc.Modal([
                dbc.ModalHeader("New Strategy"),
                dbc.ModalBody([
                    dbc.Col([
                        dbc.Row(dbc.Col(save_strategy_name)),
                        dbc.Row([
                            dbc.Col(new_frequncy_input),
                        ]),
                        dbc.Row([
                            dbc.Col(new_weighting_input),
                        ]), 
                    ])
                ]),
                dbc.ModalFooter(
                    dbc.Button("Save", id="save_strategy", className="ml-auto")
                ),
            ],
            id="strategy_modal",
        ),
    ]
)

layout = [dbc.Col([
    dbc.Row(dbc.Col(backtest_name, width=10)),
    dbc.Row([
        dbc.Col(load_symbols_dropdown, width=10),
        dbc.Col(new_symbols_button, width=2),
    ]),
    dbc.Row([
        dbc.Col(load_strategies_dropdown, width=10),
        dbc.Col(new_strategy_button, width=2),
    ]),
    dbc.Row([
        dbc.Col(save_backtest_button,),
    ]),
    symbol_modal,        
    strategy_modal,
    html.Div(id='save_backtest')
])]

@app.callback(
    Output("symbol_modal", "is_open"),
    [
        Input("new_symbols_button", "n_clicks"), 
        Input("save_symbol", "n_clicks")],
    [
        State("symbol_modal", "is_open"),
        State("save_symbol_name", "value"),
        State("new_symbols_button_dropdown", "value"),
        State("new_data_freq_input", "value"),
    ],
)
def toggle_modal(n1, n2, is_open, name, symbols, freq):
    if n1:
        all_saved_json = utils.load_local_json("Symbols")
        save_item = {
            'symbols' : symbols,
            'freq' : freq,
        }
        all_saved_json[name] = save_item
        utils.save_local_json(all_saved_json, "Symbols")
        return not is_open
    if n2: 
        return not is_open
    return is_open

@app.callback(
    Output("strategy_modal", "is_open"),
    [
        Input("new_strategy_button", "n_clicks"), 
        Input("save_strategy", "n_clicks")],
    [
        State("strategy_modal", "is_open"),
        State("save_strategy_name", "value"),
        State("new_frequncy_input", "value"),
        State("new_weighting_input", "value"),
    ],
)
def toggle_modal(n1, n2, is_open, name, freq, weight):
    if n1:
        all_saved_json = utils.load_local_json("Strategies")
        save_item = {
            'freq' : freq,
            'weight' : weight
        }
        all_saved_json[name] = save_item
        utils.save_local_json(all_saved_json, "Strategies")
        return not is_open
    if n2: 
        return not is_open
    return is_open

@app.callback(
    Output("save_backtest", "value"),
    [
        Input("save_backtest_button", "n_clicks"), 
    ],
    [
        State("backtest_name", "value"),
        State("load_symbols_dropdown", "value"),
        State("load_strategies_dropdown", "value"),
    ],
)
def save_backtest(n1, name, symbols, strategy):
    all_saved_json = utils.load_local_json("Backtests")
    saved_strategy_all = utils.load_local_json("Strategies")
    saved_symbols_all = utils.load_local_json("Symbols")
    print(strategy, symbols)
    save_item = {
        'strategy' : saved_strategy_all[strategy],
        'symbols' : saved_symbols_all[symbols]['symbols'],
        'config' : {
            'strategy' : strategy,
            'symbols' : symbols,
        }
    }
    all_saved_json[name] = save_item
    utils.save_local_json(all_saved_json, "Backtests")
    return None