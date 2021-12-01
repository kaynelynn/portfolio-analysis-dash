import os
import copy
import time
import datetime
import json
from urllib.request import pathname2url

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

from app import app
# data_dir = os.path.abspath(os.path.curdir) + "/data/"
data_dir = '/Volumes/CAPA/.storage/'
storage_dir = data_dir + "storage/"


def save_local_json(data, name):
    filepath = storage_dir + name + ".json"
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file)

def load_local_json(name):
    filepath = storage_dir + name + ".json"
    with open(filepath, 'r') as json_file:
        return json.load(json_file)

def merge_timeseries(datasets, label):
    dfs = []
    for asset, df in datasets.items():
        dfs.append(df[label].rename(asset))
    merged = pd.concat(dfs, axis=1)
    merged.ffill(inplace=True)
    merged.fillna(0, inplace=True)
    merged['time'] = merged.index
    return merged

def load_data_local(symbol):
    df = pd.read_csv(data_dir+"minute/"+symbol+'usd.csv', parse_dates=True)
    df['time'] = pd.to_datetime(df["time"], unit="ms")
    df.set_index('time',drop=False, inplace=True)
    scaled_close(df)
    df['symbol'] = symbol
    if "Unnamed: 0" in df.columns:
        del df["Unnamed: 0"]
    return df

def change_percent(frequency, dataset, append_column=True):
    # Get price value for each offset
    value = dataset["close"].pct_change(freq=frequency)
    if append_column:
        dataset[frequency+"_percent_change"] = value
    return value

def scaled_close(dataset, append_column=True):
    # Get price value for each offset
    value = dataset["close"] / max(dataset["close"])
    if append_column:
        dataset["scaled_close"] = value
    return value

def change_log(frequency, dataset, append_column=True):
    # Get price value for each offset
    if frequency+"_percent_change" in dataset:
        value = dataset[frequency+"_percent_change"].apply(lambda x: np.log(1+x))
    else:
        value = change_percent(frequency, dataset, False).apply(lambda x: np.log(1+x))
    if append_column:
        dataset[frequency+"_log_change"] = value 
    return value

def change_usd(frequency, dataset, append_column=True):
    # Get price value for each offset
    if frequency+"_percent_change" in dataset:
        value = dataset.close * dataset[frequency+"_percent_change"]
    else:
        value = dataset.close * change_percent(frequency, dataset, False)
    if append_column:
        dataset[frequency+"_usd_change"] = value 
    return dataset

def asset_statistics(datasets, frequency):
    stats = {}
    log_change = merge_timeseries(datasets, frequency + "_log_change")
    stats["var"] = log_change.var()
    stats["cov"] = log_change.cov()
    stats["corr"] = log_change.corr()
    return stats