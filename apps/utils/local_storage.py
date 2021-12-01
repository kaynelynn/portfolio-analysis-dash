import os
import copy
import time
import datetime
import json
from urllib.request import pathname2url
import pandas as pd

class LocalStorage:

    def __init__(self):
        self.data_dir = '/Volumes/CAPA/.storage/'
        self.storage_dir = self.data_dir + "storage/"  
        self.cache_dir = self.data_dir + "cache/"  
        

        # if not os.path.isdir(self.data_dir):
        #     os.mkdir(self.data_dir) 
        # if not os.path.isdir(self.storage_dir):
        #     os.mkdir(self.storage_dir) 

        self.data_dir = self.data_dir
        self.storage_dir = self.storage_dir

        # grab all minute csv file names for usd
        self.available_files = list(filter(lambda x: x.endswith("usd.csv"), os.listdir(self.data_dir)))
        # self.available_files = list(filter(lambda x: x.endswith("usd.csv"), os.listdir(self.data_dir+"minute")))
        
        

        # candles_min.write('BTCUSD', data, metadata={'source':'KuCoin'})
    def save_json(self, data, name):
        filepath = "{}{}.json".format(self.storage_dir, name)
        # print(filepath)
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def load_json(self, name):
        filepath = self.storage_dir + name
        with open(filepath, 'r') as json_file:
            return json.load(json_file)

    def save_firestore(self, data, name):
        
        filepath = "{}{}.json".format(self.storage_dir, name)
        # print(filepath)
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def load_firestore(self, name):
        filepath = self.storage_dir + name
        with open(filepath, 'r') as json_file:
            return json.load(json_file)

    # loading historical min data
    def load_csv(self, symbol):
        filepath = "{}minute/{}usd.csv".format(self.data_dir, symbol)
        df = pd.read_csv(filepath, parse_dates=True)
        df['time'] = pd.to_datetime(df["time"], unit="ms")
        df.set_index('time',drop=False, inplace=True)
        df['symbol'] = symbol
        if "Unnamed: 0" in df.columns:
            del df["Unnamed: 0"]
        return df