import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pystore
import plotly.express as px
import utils
import plotly.graph_objects as go
import pandas as pd
import ffn
import datetime
from app import app
import bt
from apps.utils.component_factory import create_text_input, create_date_input, create_dropdown_input

storage_dir = '/Volumes/CAPA/.storage'
pystore.set_path(storage_dir)
store = pystore.store('historical')
db_store = pystore.store('local_storage')
collections = store.list_collections()
collection = store.collection('Crypto.Candles')
items = collection.list_items()
saved_symbol_groups = utils.load_local_json('Symbols')
saved_strategies = utils.load_local_json('Strategies')
saved_backtests = utils.load_local_json('Backtests')
backtest_input = []
data = {}

for all_bts in saved_backtests:
    backtest_input.append({'label':all_bts,'value':all_bts})

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

load_backtest_dropdown = create_dropdown_input("Load Backtest", 'load_backtest_dropdown',initial='Default',  options=backtest_input, multi=True)


@app.callback(
    Output(component_id='bt_res', component_property='children'),
    [Input('load_backtest_dropdown', "value")],
) 
def generate_backtest(current_backtest):
    stat_layout=[]
    bts = []
    for b in current_backtest:
        current_config = saved_backtests[b]
        symbols = current_config['symbols']
        datasets = {}
        current_bars = []
        current_freq = frequency_algos[current_config['strategy']['freq']]
        current_weighting = weighting_algos[current_config['strategy']['weight']]
        for symbol in symbols:
            datasets[symbol] = collection.item(symbol + "/Day").to_pandas()
        closing_prices = merge_timeseries(datasets, 'close')
        # filtered_datasets = datasets[start:end]
        current_strategy = bt.Strategy(b,
            [
                current_freq,
                bt.algos.SelectHasData(),
                current_weighting,
                bt.algos.Rebalance()
            ]
        )
        current_bt = bt.Backtest(current_strategy, closing_prices)
        bts.append(current_bt)

    current_res = bt.run(*bts)
    # stats_to_get = ['total_return', 'monthly_sharpe', 'max_drawdown', 'cagr', 'ytd', 'daily_sharpe','monthly_vol','avg_drawdown', 'avg_drawdown_days', 'avg_up_month', 'avg_down_month']
    # pretty = current_res.stats.loc[['total_return', 'monthly_sharpe', 'max_drawdown', 'cagr', 'ytd', 'daily_sharpe','monthly_vol','avg_drawdown', 'avg_drawdown_days', 'avg_up_month', 'avg_down_month'], :].T.sort_values('total_return', ascending=False)
    # return "Total return: {} x".format(total_return)
    stat_layout.append(html.H1(b))
    for x in strategy_stats:
        row_layout = []

        if x == 'metrics_total':
            for y in strategy_stats[x]:
                subrow_layout = []
                subrow_layout.append(dbc.Col(html.H3(y)))
                for xy in strategy_stats[x][y]:
                    stat
                    # if xy[2] == 'p':
                    #     # stat = ffn.utils.fmtp(stat)
                    #     stat = stat
                    # elif xy[2] == 'n':
                    #     stat = stat
                    #     # stat = ffn.utils.fmtn(stat)
                    # elif xy[2] == 'dt':
                    #     stat = stat
                    #     # stat = pd.to_datetime(stat)
                    for currentbt in current_backtest:
                        stat = current_res.stats.loc[[xy[0], currentbt]]

                        print(stat)
                        fig = [go.Bar(x=currentbt, y=stat.loc[currentbt])]
                        current_bars.append(fig)

                    # stat.transpose()
                    # print(px.data.medals_long())
                    stat_card = dbc.Col([
                        html.H5(xy[1]),
                        dcc.Graph(id='test_fig', figure=go.Figure(fig))
                        ],
                        width='auto')
                    subrow_layout.append(stat_card)
                row_layout.append(dbc.Row(subrow_layout))
        else: 
            for z in strategy_stats[x]:
                stat = current_res.stats.loc[z[0]]
                if z[2] == 'p':
                    # stat = ffn.utils.fmtp(stat)
                    stat = stat
                elif z[2] == 'n':
                    stat = stat
                    # stat = ffn.utils.fmtn(stat)
                # elif z[2] == 'dt':
                    # stat = datetime.datetime.fromtimestamp(stat)
                stat_card = dbc.Col([html.H4(z[1]), html.P(stat)], width='auto')
                row_layout.append(stat_card)
        stat_layout.append(html.H2(x))
        stat_layout.append(dbc.Row(row_layout))
        stat_layout.append(html.Br())
    # reload_saved_files()

    # columns=[{"name": i, "id": i} for i in current_res.stats.columns],
    # print(list(current_res.stats['test'].to_dict().items()))
    # return list(current_res.stats['test'].to_dict().items())
    # return 
    return html.Div(stat_layout)
layout = [
    dbc.Col([
        load_backtest_dropdown,
        html.Div(id='bt_res'),
        ])
]

def merge_timeseries(datasets, label):
    dfs = []
    for asset, df in datasets.items():
        dfs.append(df[label].rename(asset))
    merged = pd.concat(dfs, axis=1)
    merged.ffill(inplace=True)
    # merged.fillna(0, inplace=True)
    return merged