import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def create_input(label, id, placeholder, input_type, initial, **kwargs):
    input_types = ["text", "date", "number"]
    selection_types = ["checklist", "dropdown"]
    if input_type in input_types:
        component = dbc.Input(
                        type=input_type,
                        id=id,
                        placeholder=placeholder,
                        value=initial
                    )
    else:
        args = {
            "options": kwargs["options"],
            "id":id,
            "value":initial,
        }
        if input_type == "dropdown":
            args['multi'] = kwargs.get('multi', False)
            Component = dcc.Dropdown
            args["placeholder"] = placeholder
        elif input_type == "checklist":
            Component = dbc.Checklist
        component = Component(**args)
    return dbc.FormGroup(
        [
            dbc.Label(label, width=3),
            dbc.Col(
                component,
                width=9,
            ),
        ],
        row=True,
    )

def create_text_input(label, id, placeholder, initial="", **kwargs):
    return create_input(label, id, placeholder, "text", initial, **kwargs)

def create_date_input(label, id, placeholder, initial="", **kwargs):
    return create_input(label, id, placeholder, "date", initial, **kwargs)

def create_number_input(label, id, placeholder, initial=0, **kwargs):
    return create_input(label, id, placeholder, "number", initial, **kwargs)

def create_dropdown_input(label, id, placeholder=None, initial=[], **kwargs):
    return create_input(label, id, placeholder, "dropdown", initial, **kwargs)

def create_checklist_input(label, id, placeholder=None, initial=[], **kwargs):
    return create_input(label, id, placeholder, "checklist", initial, **kwargs)

def create_card_list(values):
    charts = []
    for value in values:
        # card = dbc.Card(
        # [
        #     dbc.CardBody(
        #         [
        #             html.H4(key['label'], className="card-title"),
        #             dcc.Loading(id="chart_loading", children=[dcc.Graph(id={'type':'current_figure', 'index': key['value']})], type="default"),
        #             html.P(key['value'],
        #                 className="card-text",
        #             ),
        #             dbc.Button('View Report',id={'type': 'load_graph_button', 'index': key['value']},
        #                 outline=True),
        #         ]
        #     ),
        # ],
        # id="report-card"
        # )
        card = create_report_card(value)
        charts.append(html.Br())
        charts.append(card)
    return charts


def create_report_card(value):
    card = dbc.Card(
        [dbc.CardBody(
            [dbc.Row([
            dbc.Col(html.H4(value['label'])), 
            dbc.Col(html.P(["File: " + value['value']],className="card-text",style={'textAlign':'center',"paddingTop":12})),
            dbc.Col(dbc.Button('View Report',id={'type': 'load_graph_button', 'index': value['value']}, color='primary'),id='view_graph_button_col'), 
            ]),
            dbc.Row(dbc.Col(dcc.Loading(id="chart_loading", children=[dcc.Graph(id={'type':'current_figure', 'index': value['value']})], type="default"),)),
            ]
        )
        ]
    )
    return card