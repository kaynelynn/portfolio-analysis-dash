import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from apps import menu, explore, create_report, create_backtest, create_backtest_form, backtest_analysis
# from apps.Layout import test
from apps.Examples import load_local_json_graph, save_local_json_graph

content = dbc.Col(
    [dcc.Location(id='url', refresh=False),
    html.Div(id="page_content")
    ],
    width=True)

app.layout = dbc.Container([
    dbc.Row(menu.topbar),
    dbc.Row([
        menu.sidebar,
        content
    ])
]
)

@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/explore':
        return explore.layout
    elif pathname == '/test':
        return backtest_analysis.layout
    elif pathname == '/test2':
        return create_backtest_form.layout        
    else:
        return create_report.layout

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)