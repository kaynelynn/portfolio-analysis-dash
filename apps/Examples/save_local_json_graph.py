# import os
# from re import A
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output, State
# import plotly.express as px

# from app import app
# import utils

# available_files = os.listdir(utils.data_dir + "minute")
# print(utils.storage_dir)
# data = {}
# symbols = []
# frequencies = ["1D"]
# available_symbols = []
# available_frequencies = []

# for fileName in available_files:
#     if fileName.endswith("usd.csv"):
#         name = fileName[0:-7]
#         available_symbols.append({'label':name,'value':name})

# chart_name_input = dbc.FormGroup(
#     [
#         dbc.Label("Chart Name", width=2),
#         dbc.Col(
#             dbc.Input(
#                 type="text", id="chart_name_input", value="2015-2016 MegaCap Minutely"
#             ),
#             width=10,
#         ),
#     ],
#     row=True,
# )

# chart_start_input = dbc.FormGroup(
#     [
#         dbc.Label("Analysis Start Date", width=2),
#         dbc.Col(
#             dbc.Input(
#                 type="date",
#                 id="chart_start_input",
#                 placeholder="Select a start date.",
#                 value="2019-01-01"
#             ),
#             width=10,
#         ),
#     ],
#     row=True,
# )

# chart_end_input = dbc.FormGroup(
#     [
#         dbc.Label("Analysis End Date", width=2),
#         dbc.Col(
#             dbc.Input(
#                 type="date",
#                 id="chart_end_input",
#                 placeholder="Select an end date.",
#                 value="2020-05-01"
#             ),
#             width=10,
#         ),
#     ],
#     row=True,
# )

# chart_symbols_input = dbc.FormGroup(
#     [
#         dbc.Label("Select Assets to Include", width=2),
#         dbc.Col(
#             dbc.Checklist(
#                 options=sorted(available_symbols, key = lambda i: i['label']),
#                 value=[],
#                 id="chart_symbols_input",
#         ),
#         width=10,
#         )
#     ],
#     row=True,
# )

# save_chart_button = dbc.Button("Update Graph", color="primary", id="update_saved_chart_button", outline=True, block=True)
# update_saved_chart_button = dbc.Button("Save Graph", color="primary", id="save_chart_button", outline=True, block=True)

# layout = [
#     dcc.Store(id="store"),
#     dbc.Form([
#         chart_name_input,
#         chart_start_input, 
#         chart_end_input, 
#         chart_symbols_input,
#         html.Div([html.Br(), update_saved_chart_button], id="submit_button_row"),
#         html.Div([html.Br(), save_chart_button], id="submit_button_row")]),
#     html.Br(),
#     html.Div(id='new_symbol_list'),
#     html.Div(id='new_date_range'),
#     html.Div(id='save_config_output'),
#     dcc.Loading(id="chart_loading", children=[dcc.Graph(figure={}, id='new_chart_data')], type="default"),
# ]

# @app.callback(
#     Output(component_id='save_config_output', component_property='value'),
#     [Input('save_chart_button', "n_clicks")],
#     State('chart_start_input', 'value'),
#     State('chart_end_input', 'value'),
#     State('chart_name_input', 'value'),
# )
# def save_config(n, start, end, name):
#     config = {
#         'start': start,
#         'end': end,
#         'title': name,
#         'symbols': list(data.keys()),
#         'hover_data':{
#             "time": "|%B %d, %Y"
#             },
#         'layout': {
#             'xaxis_title' : 'Date',
#             'yaxis_title' : 'f\'Scaled Close\'',
#             },
#         'xaxes': {
#             'value': "time",
#             'dtick':"M1",
#             'tickformat':"%b\n%Y",
#         },
#         'yaxes': {
#             'value': list(data.keys()),
#         },
#     }
#     utils.save_local_json(config, name)
#     return 

# @app.callback(
#     Output(component_id='new_chart_data', component_property='figure'),
#     [Input('update_saved_chart_button', "n_clicks")],
#     State('chart_start_input', 'value'),
#     State('chart_end_input', 'value'),
#     State('chart_name_input', 'value'),
# )
# def update_saved_graph(n, start, end, name):
#     config = {
#         'start': start,
#         'end': end,
#         'title': name,
#         'symbols': list(data.keys()),
#         'hover_data':{
#             "time": "|%B %d, %Y"
#             },
#         'layout': {
#             'xaxis_title' : 'Date',
#             'yaxis_title' : 'f\'Scaled Close\'',
#             },
#         'xaxes': {
#             'value': "time",
#             'dtick':"M1",
#             'tickformat':"%b\n%Y",
#         },
#         'yaxes': {
#             'value': list(data.keys()),
#         },
#     }
#     if len(data.keys()) > 1:
#         df = utils.merge_timeseries(data, "scaled_close", "1H")[start:end]
#         print(df, name, 'Complete. Sample Data above')
#         fig = px.line(df, x="time", y=df.columns,
#               hover_data={"time": "|%B %d, %Y"},
#               )
#         fig.update_layout(
#             title = name,
#             xaxis_title = 'Date',
#             yaxis_title = f'Scaled Close',
#         )
#         fig.update_xaxes(
#             dtick="M1",
#             tickformat="%b\n%Y")
#         return fig
#     else:
#         print(data)
#         return {}

# @app.callback(
#     Output(component_id='new_symbol_list', component_property='value'),
#     Input(component_id='chart_symbols_input', component_property='value')
# )
# def update_saved_symbols(input_value):
#     for symbol in input_value:
#         data[symbol] = utils.load_data_local(symbol)
#     return input_value
#         # utils.change_percent(frequency, data[symbol])
#         # utils.change_log(frequency, data[symbol])
#         # utils.change_usd(frequency, data[symbol])
  

# @app.callback(
#     Output(component_id='chart_name_output', component_property='children'),
#     Input(component_id='chart_name_input', component_property='value')
# )
# def update_saved_symbols(input_value):
#     return input_value

# @app.callback(
#     Output('new_date_range', 'children'),
#     [Input('new_date_range_picker', 'chart_start_input'),
#     Input('new_date_range_picker', 'chart_end_input')])
# def update_saved_new_date_range(start_date, end_date):
#     print("update")
#     for symbol in data.keys():
#         data[symbol] = data[symbol][start_date:end_date]
#     return start_date, end_date
