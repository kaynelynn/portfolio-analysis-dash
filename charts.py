from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px

from app import app, server, cache
import utils

def scaled_close_scatter(datasets):
    fig = go.Figure()
    merged = utils.merge_timeseries(datasets, "scaled_close")
    merged.resample("1D")
    for symbol in datasets.keys():
        fig.add_trace(
            go.Scatter(
                x = merged.index,
                y = merged[symbol],
                name = symbol
            )
    )
    return fig
        

