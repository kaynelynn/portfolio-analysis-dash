import os
import dash
import dash_bootstrap_components as dbc
# from flask_caching import Cache

from apps.utils.local_storage import LocalStorage

storage = LocalStorage()

CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': storage.cache_dir
}


# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.CYBORG]

app = dash.Dash(__name__)
# cache = Cache(app.server, config=CACHE_CONFIG)
app.config.suppress_callback_exceptions = True
