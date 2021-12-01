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

import inspect
from html.parser import HTMLParser
import dash_html_components as html
class DashHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stack = []
        self.dash_object = None

    @staticmethod
    def get_dash_tag_class(tag):
        tag_title = tag.title()
        if not hasattr(html, tag_title):
            raise ValueError(f'Can not find Dash HTML tag {tag_title}')

        return getattr(html, tag_title)

    def handle_starttag(self, tag, attrs):
        dash_tag_class = self.get_dash_tag_class(tag)

        # Convert Attributes to Dash Attributes
        dash_attrs = {}
        if attrs:
            named_dash_attrs = list(inspect.signature(dash_tag_class.__init__).parameters)[1:-1]
            lower_named_dash_attrs = {n.lower(): n for n in named_dash_attrs}
            for attr_name, attr_value in attrs:
                lower_attr_name = attr_name.lower()
                if lower_attr_name == 'class':
                    dash_attrs['className'] = attr_value
                elif lower_attr_name == 'style':
                    style_dict = {}
                    for style in attr_value.split(';'):
                        style_key, style_value = style.split(':')
                        style_dict[style_key] = style_value
                    dash_attrs['style'] = style_dict
                elif lower_attr_name in ('n_clicks', 'n_clicks_timestamp'):
                    dash_attrs[lower_attr_name] = int(attr_value)
                elif lower_attr_name in lower_named_dash_attrs:
                    dash_attrs[lower_named_dash_attrs[lower_attr_name]] = attr_value
                else:
                    dash_attrs[attr_name] = attr_value
        
        # Create the real tag
        dash_tag = dash_tag_class(**dash_attrs)
        self._stack.append(dash_tag)

    def handle_endtag(self, tag):
        dash_tag_class = self.get_dash_tag_class(tag)
        dash_tag = self._stack.pop()
        if type(dash_tag) is not dash_tag_class:
            raise ValueError(f'Malformed HTML')

        # Final Tag
        if not self._stack:
            self.dash_object = dash_tag
            return

        # Set Children to always be a list
        if type(self._stack[-1].children) is not list:
            self._stack[-1].children = []

        # Append tag on to parent tag
        self._stack[-1].children.append(dash_tag)

    def handle_data(self, data):
        # Set Children to always be a list
        if type(self._stack[-1].children) is not list:
            self._stack[-1].children = []

        # Append tag on to parent tag
        self._stack[-1].children.append(data)


def html_to_dash(html_string):
    parser = DashHTMLParser()
    parser.feed(html_string)
    return parser.dash_object

from messari import Messari
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import os
from apps.utils.local_storage import LocalStorage
storage = LocalStorage()
import time
messari = Messari('')
# res = messari.get_all_assets()['data']
stored_assets = os.listdir(storage.storage_dir)
# all_assets = []
# for result in res:
#     all_assets.append(result)
# i = 310
# while len(res) > 0:
# # while i < 5:
#     res = messari.get_all_assets(page = i)
#     if 'data' in res: 
#         for result in res['data']: 
#             all_assets.append(result)
#             messari_name = result['name']
#             messari_slug = result['slug']
#             symbol = result['symbol']
#             messari_id = result['id']
#             if type(messari_slug) == str:
#                 storage.save_json(result, "messari-all-"+messari_slug)
#                 print("saved ", messari_slug)
#             elif type(symbol) == str:
#                 storage.save_json(result, "messari-all-"+symbol)
#                 print("saved ", symbol)
#             elif type(messari_name) == str:
#                 storage.save_json(result, "messari-all-"+messari_name.replace("/","-"))
#                 print("saved ", messari_name.replace("/","-"))
#         time.sleep(2.5)
#         print("getting more current page",i,"\nlength", len(all_assets))
#     else:
#         break
#     i += 1
asset_cards = []
for asset in stored_assets:
    asset = storage.load_json(asset)
    messari_name = asset['name']
    messari_slug = asset['slug']
    messari_id = asset['id']
    symbol = asset['symbol']
    #labels, etc
    overview = asset['profile']['general']['overview']
    is_verified = overview['is_verified']
    tagline = overview['tagline']
    category = overview['category']
    sector = overview['sector']
    tags = overview['tags']
    project_details = overview['project_details']

    # organization, background, links
    background_details = asset['profile']['general']['background']['background_details']
    organization = asset['profile']['general']['background']['issuing_organizations']
    links = overview['official_links']

    # Roadmap
    roadmap = asset['profile']['general']['roadmap']

    # weird regulation thing
    regulation = asset['profile']['general']['regulation']

    #People and Orgs - gives people and orgs
    ind_contributors = asset['profile']['contributors']['individuals']
    org_contributors = asset['profile']['contributors']['organizations']
    ind_advisors = asset['profile']['advisors']['individuals']
    org_advisors = asset['profile']['advisors']['organizations']
    ind_investors = asset['profile']['investors']['individuals']
    org_investors = asset['profile']['investors']['organizations']

    #Ecosystem?

    ecosystem_assets = asset['profile']['ecosystem']['assets']
    ecosystem_orgs = asset['profile']['ecosystem']['organizations']

    # Economics

    token_details = asset['profile']['economics']['token']
    launch_details = asset['profile']['economics']['launch']
    consensus_details = asset['profile']['economics']['consensus_and_emission']
    treasury_details = asset['profile']['economics']['native_treasury']

    # Tecnology
    tech_details = asset['profile']['technology']['overview']['technology_details']
    client_repositories = asset['profile']['technology']['overview']['client_repositories']
    security_audits = asset['profile']['technology']['security']['audits']
    known_exploits = asset['profile']['technology']['security']['known_exploits_and_vulnerabilities']

    # Governance
    gov_details = asset['profile']['governance']['governance_details']
    gov_onchain = asset['profile']['governance']['onchain_governance']
    gov_grants = asset['profile']['governance']['grants']

    price = asset['metrics']['market_data']['price_usd']
    if type(price) == float:
        price_formatted = "${:,.4f}".format(price)

        card = dbc.Card([
            dbc.Col([
                dbc.Row([
                dbc.Col([html.H2(messari_name), html.H5(tagline)]),
                dbc.Col([html.H2(price_formatted), html.H5([category,", ", sector, "\n",tags])]),
                ]),
                # dbc.Col(["Project Details: ", html.Br(), html_to_dash("<span>" + project_details + '</span>'), html.Br(),html.Br(), ]),
                # dbc.Col(["Background Details: ", html.Br(), html_to_dash("<span>" + background_details + '</span>')]),
            ])
            ]
        )

        asset_cards.append(html.Br())
        asset_cards.append(card)

layout = dbc.Col(
    asset_cards
)

