import utils
import plotly.express as px

# config = {
    #     'start': start,
    #     'end': end,
    #     'title': name,
    #     'symbols': list(data.keys()),
    #     'hover_data':{
    #         "time": "|%B %d, %Y"
    #         },
    #     'layout': {
    #         'xaxis_title' : 'Date',
    #         'yaxis_title' : 'f\'Scaled Close\'',
    #         },
        # 'xaxes': {
        #     'value': "time",
        #     'dtick':"M1",
        #     'tickformat':"%b\n%Y",
        # },
    #     'yaxes': {
    #         'value': list(data.keys()),
    #     },
    #     # 'frequencies': frequencies,
    #     # 'sample': sample,
    # }

class Chart:

    default_timeseries_style = {
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
    }

    def __init__(self, data, config={}):
        self.loaded = False 
        self.fig = None
        self.data = data
        self.config = self.apply_config(config)

    def apply_config(self, config):
        self.config = {
            **config,
            **Chart.default_style,
            'yaxes': {
                'value': list(self.data.keys()),
            }
        }



    def load(self):
        # load chart metadata from json file then generate
        pass 

    def save(self):
        # save chart metadata to json file
        pass

    def generate(self, merge_key, sample):
        # generate new chart
        df = utils.merge_timeseries(self.data, merge_key, sample)

        fig = px.line(
            df, 
            x=self.config['xaxes']['value'], 
            y=self.config['yaxes']['value'], 
            hover_data=self.config['hover_data']
        )
        fig.update_layout(
            title = self.config['title'],
            xaxis_title = self.config['layout']['xaxis_title'],
            yaxis_title = self.config['layout']['yaxis_title'],
        )
        fig.update_xaxes(
            dtick=self.config['xaxes']['dtick'],
            tickformat=self.config['xaxes']['tickformat'])
        self.fig = fig
        return fig




















# temp function - start using class method 
def generate_chart(title, data, merge_key, hover_data, layout, 
    yaxes={
        'xaxis_title' : 'Date',
        'yaxis_title' : 'f\'Scaled Close\'',
    },
    xaxes={
        'value': "time",
        'dtick':"M1",
        'tickformat':"%b\n%Y",
    }, 
    sample="1H"):
        df = utils.merge_timeseries(data, merge_key, sample)

        fig = px.line(df, x=xaxes['value'], y=yaxes['value'], hover_data=hover_data)
        fig.update_layout(
            title = title,
            xaxis_title = layout['xaxis_title'],
            yaxis_title = layout['yaxis_title'],
        )
        fig.update_xaxes(
            dtick=xaxes['dtick'],
            tickformat=xaxes['tickformat'])
        return fig