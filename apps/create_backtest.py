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
storage_dir = '/Volumes/CAPA/.storage'
data = {}
pystore.set_path(storage_dir)
store = pystore.store('historical')
db_store = pystore.store('local_storage')
collections = store.list_collections()
collection = store.collection('Crypto.Candles')
items = collection.list_items()
data = {}
all_symbols = []
all_symbols_input =[]
saved_symbol_groups = utils.load_local_json('Symbols')
saved_symbol_groups_input =[]
saved_dates = utils.load_local_json('Dates')
saved_dates_input =[]
saved_strategies = utils.load_local_json('Strategies')
saved_strategies_input =[]

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
for strat in saved_strategies: 
    saved_strategies_input.append({
        'label' : strat,
        'value' : strat
    }) 

def reload_saved_files():
    saved_symbol_groups = utils.load_local_json('Symbols')
    saved_symbol_groups_input =[]
    saved_dates = utils.load_local_json('Dates')
    saved_dates_input =[]
    saved_strategies = utils.load_local_json('Strategies')
    saved_strategies_input =[]
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
    for backt in saved_strategies: 
        saved_strategies_input.append({
            'label' : backt,
            'value' : backt
    }) 

reload_saved_files()

for s in items:
    all_symbols.append(s)

for available_symbol in all_symbols:
    all_symbols_input.append({'label':available_symbol,'value':available_symbol})

def merge_timeseries(datasets, label):
    dfs = []
    for asset, df in datasets.items():
        dfs.append(df[label].rename(asset))
    merged = pd.concat(dfs, axis=1)
    merged.ffill(inplace=True)
    # merged.fillna(0, inplace=True)
    return merged

my_symbols = [
    "ETH",
    "BTC",
    "MATIC",
    "CRO",
    "FIL",
    "UNI",
    "BAT",
    "LINK",
    "GRT",
    "AAVE",
    "COMP",
    "SNX"
]

backtest_data_frequencies = [
    {'label' : 'Day',
    'value' :  '/Day',},
    {'label' : 'Minute',
    'value' : '/Min'}
]

save_options = [
    {'label' : 'Strategy',
    'value' :  'Strategies',},
    {'label' : 'Symbols',
    'value' : 'Symbols'},
    {'label' : 'Dates',
    'value' : 'Dates'}
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

frequency_algos = {
    'once':  bt.algos.RunOnce(),
    'weekly' :  bt.algos.RunWeekly(),
    'monthly' : bt.algos.RunMonthly(),
    'quarterly': bt.algos.RunQuarterly(),
    'yearly': bt.algos.RunYearly(),
}

weighting_algos = {
    'equal':  bt.algos.WeighEqually(),
    'inv-var' :  bt.algos.WeighInvVol(),
    'mean-var' : bt.algos.WeighMeanVar(),
    'erc': bt.algos.WeighERC(),
}

strategy_stats = {
    'details' : [
        ('start', 'Start', 'dt'),
        ('end', 'End', 'dt'),
    ],
    'metrics_total' : {
        'overview' : [
        ('total_return', 'Total Return', 'p'),
        ('cagr', 'CAGR', 'p'),
        ('rf', 'Risk-free rate', 'p'),
        ],
        'ratios' : [
        ('daily_sharpe', 'Daily Sharpe', 'n'),
        ('monthly_sharpe', 'Monthly Sharpe', 'n'),
        ('yearly_sharpe', 'Yearly Sharpe', 'n'),
        ('calmar', 'Calmar Ratio', 'n'),
        ],
        'returns' : [
        ('total_return', 'Total Return', 'p'),
        ('mtd', 'MTD', 'p'),
        ('three_month', '3m', 'p'),
        ('six_month', '6m', 'p'),
        ('ytd', 'YTD', 'p'),
        ('one_year', '1Y', 'p'),
        ('three_year', '3Y (ann.)', 'p'),
        ('five_year', '5Y (ann.)', 'p'),
        ('ten_year', '10Y (ann.)', 'p'),
        ('incep', 'Since Incep. (ann.)', 'p'),
        ],
        'drawdown' : [
        ('max_drawdown', 'Max Drawdown', 'p'),
        ('avg_drawdown', 'Avg. Drawdown', 'p'),
        ('avg_drawdown_days', 'Avg. Drawdown Days', 'n'),
        ('win_year_perc', 'Win Year %', 'p'),
        ('twelve_month_win_perc', 'Win 12m %', 'p')
        ]

    },
    'metrics_daily' : [
        ('daily_sortino', 'Daily Sortino', 'n'),
        ('daily_mean', 'Daily Mean (ann.)', 'p'),
        ('daily_vol', 'Daily Vol (ann.)', 'p'),
        ('daily_skew', 'Daily Skew', 'n'),
        ('daily_kurt', 'Daily Kurt', 'n'),
        ('best_day', 'Best Day', 'p'),
        ('worst_day', 'Worst Day', 'p'),
    ],
    'metrics_monthly' : [
        ('monthly_sortino', 'Monthly Sortino', 'n'),
        ('monthly_mean', 'Monthly Mean (ann.)', 'p'),
        ('monthly_vol', 'Monthly Vol (ann.)', 'p'),
        ('monthly_skew', 'Monthly Skew', 'n'),
        ('monthly_kurt', 'Monthly Kurt', 'n'),
        ('best_month', 'Best Month', 'p'),
        ('worst_month', 'Worst Month', 'p'),
        ('avg_up_month', 'Avg. Up Month', 'p'),
        ('avg_down_month', 'Avg. Down Month', 'p'),
    ],
    'metrics_yearly' : [
        ('yearly_sortino', 'Yearly Sortino', 'n'),
        ('yearly_mean', 'Yearly Mean', 'p'),
        ('yearly_vol', 'Yearly Vol', 'p'),
        ('yearly_skew', 'Yearly Skew', 'n'),
        ('yearly_kurt', 'Yearly Kurt', 'n'),
        ('best_year', 'Best Year', 'p'),
        ('worst_year', 'Worst Year', 'p'),
    ]
}

# title
strategy_name_input = create_text_input("Name", "strategy_name_input", "2015-2016 MegaCap Minutely",initial='test')

# date range
strategy_start_input = create_date_input("Start Date", "strategy_start_input", "Select a start date.","2018-01-01")
strategy_end_input = create_date_input("End Date", "strategy_end_input", "Select an end date.","2021-06-01")

#frequency
strategy_frequncy_input = create_dropdown_input("Frequency", 'strategy_frequncy_input', initial='weekly', options=strategy_frequencies)
strategy_weighting_input = create_dropdown_input("Weighting", 'strategy_weighting_input', initial='equal',  options=strategy_weightings)
strategy_data_freq_input = create_dropdown_input("Data Freq", 'strategy_data_freq_input', initial='/Day',  options=backtest_data_frequencies)
generate_backtest_button = dbc.Button("Run Backtest", color="primary", id="generate_backtest_button", block=True)

save_name = create_text_input("Choose a name to save your configuration.", "save_name", None, initial="Default")
save_dropdown = create_dropdown_input("Save Config", 'save_dropdown', initial='Symbols', options=save_options)
save_button = dbc.Button("Save", color="primary", id="save_button", block=True)


load_symbols_dropdown = create_dropdown_input("Load Symbols Group", 'load_symbols_dropdown',initial=['Default'], options=saved_symbol_groups_input, multi=True)
load_dates_dropdown = create_dropdown_input("Load Dates", 'load_dates_dropdown',initial=['Default'],  options=saved_dates_input)
load_strategies_dropdown = create_dropdown_input("Load Backtest", 'load_strategies_dropdown',initial=['Default'],  options=saved_strategies_input)

# symbols
# backtest_symbols_input = create_checklist_input("Assets to Include", "backtest_symbols_input", initial=my_symbols, options=sorted(all_symbols_input, key = lambda i: i['label']))
backtest_symbols_input = create_dropdown_input("Assets to Include:", 'backtest_symbols_input', initial=my_symbols,  options=sorted(all_symbols_input, key = lambda i: i['label']), multi=True)
# backtest_symbols_input = dbc.Col([dbc.FormGroup(
#         [
#             dbc.Label("Assets to Include:", width=4),
#             dbc.Col(
#                 dcc.Dropdown(
#                     id='backtest_symbols_input',
#                     options=sorted(all_symbols_input, key = lambda i: i['label']),
#                     value=my_symbols,
#                     multi=True
#                     ),
#                 width=8,
#             ),
#         ],
#         # row=True,
#     )
# ], width=12)
    
backtest_form = dbc.Form(
    [   dbc.Row(
            [
                dbc.Col(
                    strategy_name_input,
                    width=4,
                ),
                dbc.Col(
                    strategy_start_input,
                    width=4,
                ),
                dbc.Col(
                    strategy_end_input,
                    width=4,
                ),    
                           
            ]
        ),
        
        dbc.Row(
            [
                dbc.Col(
                    strategy_data_freq_input,
                    width=4,
                ),
                dbc.Col(
                    strategy_frequncy_input,
                    width=4,
                ),
                dbc.Col(
                    strategy_weighting_input,
                    width=4,
                ),    
                           
            ]
        ),
        backtest_symbols_input,
        dbc.Row(
            [
                dbc.Col(
                    load_strategies_dropdown,
                    width=4,
                ),
                dbc.Col(
                    load_symbols_dropdown,
                    width=4,
                ),
                dbc.Col(
                    load_dates_dropdown,
                    width=4,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    save_dropdown,
                    width=4,
                ),
                dbc.Col(
                    save_name,
                    width=4,
                ),
                dbc.Col(
                    save_button,
                    width=4,
                ),
            ],
            form=True,
        ),
        dbc.Col(
            generate_backtest_button,
            width=12,
            style={'padding-left':'25%', 'padding-right':'25%', 'padding-top':20}
        ),
         
    ]
)

@app.callback(
    Output(component_id='save_output', component_property='value'),
    [Input('save_button', "n_clicks")],
    State('backtest_symbols_input', 'value'),
    State('strategy_start_input', 'value'),
    State('strategy_end_input', 'value'),
    State('strategy_data_freq_input', 'value'),
    State('strategy_frequncy_input', 'value'),
    State('strategy_weighting_input', 'value'),
    State('save_dropdown', 'value'),
    State('save_name', 'value'),
) 
def save_config(n, symbols, start, end, data_freq, freq, weighting, current_val, current_name):
    all_saved_json = utils.load_local_json(current_val)
    save_item = {}
    save_val = {}
    if current_val == "Symbols":
        save_item = {
            'start' : start,
            'end' : end,
            'symbols' : symbols,
            'data_freq' : data_freq,
        }
    elif current_val == "Strategies":
        save_item = {
            'frequency' : freq,
            'weighting' : weighting,
        }
    all_saved_json[current_name] = save_item
    utils.save_local_json(all_saved_json, current_val)
    reload_saved_files()

@app.callback(
    Output(component_id='backtest_table', component_property='children'),
    [Input('generate_backtest_button', "n_clicks")],
    State('strategy_name_input', 'value'),
    State('strategy_start_input', 'value'),
    State('strategy_end_input', 'value'),
    State('backtest_symbols_input', 'value'),
    State('strategy_data_freq_input', 'value'),
    State('strategy_frequncy_input', 'value'),
    State('strategy_weighting_input', 'value'),
) 
def generate_backtest(n, name, start, end, symbols, data_freq, freq, weighting):
    datasets = {}
    current_freq = frequency_algos[freq]
    current_weighting = weighting_algos[weighting]
    for symbol in symbols:
        datasets[symbol] = collection.item(symbol + data_freq).to_pandas()
    closing_prices = merge_timeseries(datasets, 'close')
    # filtered_datasets = datasets[start:end]
    current_strategy = bt.Strategy(name,
        [
            current_freq,
            bt.algos.SelectHasData(),
            current_weighting,
            bt.algos.Rebalance()
        ]
    )
    current_backtest = bt.Backtest(current_strategy, closing_prices)
    current_res = bt.run(current_backtest)
    # stats_to_get = ['total_return', 'monthly_sharpe', 'max_drawdown', 'cagr', 'ytd', 'daily_sharpe','monthly_vol','avg_drawdown', 'avg_drawdown_days', 'avg_up_month', 'avg_down_month']
    # pretty = current_res.stats.loc[['total_return', 'monthly_sharpe', 'max_drawdown', 'cagr', 'ytd', 'daily_sharpe','monthly_vol','avg_drawdown', 'avg_drawdown_days', 'avg_up_month', 'avg_down_month'], :].T.sort_values('total_return', ascending=False)
    # return "Total return: {} x".format(total_return)
    stat_layout = []
    for x in strategy_stats:
        row_layout = []
        if x == 'metrics_total':
            for y in strategy_stats[x]:
                subrow_layout = []
                subrow_layout.append(dbc.Col(html.H3(y)))
                for xy in strategy_stats[x][y]:
                    stat = current_res.stats.loc[xy[0], name]
                    if xy[2] == 'p':
                        stat = ffn.utils.fmtp(stat)
                    elif xy[2] == 'n':
                        stat = ffn.utils.fmtn(stat)
                    elif xy[2] == 'dt':
                        stat = pd.to_datetime(stat)
                    stat_card = dbc.Col([html.H5(xy[1]), html.P(stat)], width='auto')
                    subrow_layout.append(stat_card)
                row_layout.append(dbc.Row(subrow_layout))
        else: 
            for z in strategy_stats[x]:
                stat = current_res.stats.loc[z[0], name]
                if z[2] == 'p':
                    stat = ffn.utils.fmtp(stat)
                elif z[2] == 'n':
                    stat = ffn.utils.fmtn(stat)
                elif z[2] == 'dt':
                    stat = datetime.date(stat)
                stat_card = dbc.Col([html.H4(z[1]), html.P(stat)], width='auto')
                row_layout.append(stat_card)
        stat_layout.append(html.H2(x))
        stat_layout.append(dbc.Row(row_layout))
        stat_layout.append(html.Br())
    reload_saved_files()

    # columns=[{"name": i, "id": i} for i in current_res.stats.columns],
    # print(list(current_res.stats['test'].to_dict().items()))
    # return list(current_res.stats['test'].to_dict().items())
    return stat_layout

layout = [
    backtest_form, 
    dbc.Col(
        id='backtest_table',
    ),
    dbc.Col([],
        id='save_output',
    )
]

def reload_saved_files():
    saved_symbol_groups = utils.load_local_json('Symbols')
    saved_symbol_groups_input =[]
    saved_dates = utils.load_local_json('Dates')
    saved_dates_input =[]
    saved_strategies = utils.load_local_json('Strategies')
    saved_strategies_input =[]
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

    for backt in saved_strategies: 
        saved_strategies_input.append({
            'label' : backt,
            'value' : backt
        })   

