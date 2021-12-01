import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app

menu = [
    dbc.NavItem(dbc.NavLink(dcc.Link('Home', href='/'), href='/')),
    dbc.NavItem(dbc.NavLink(dcc.Link('Explore', href='/explore'), href='/explore')),
]

navbar = dbc.Nav(
    menu,
    vertical=True,
    pills=True,
    justified=True,
    id='nav_bar',
)

sidebar = dbc.Col([
    html.Div(
        [
        navbar,
        ],
    )
], width='auto'
)

topbar = dbc.Col(
    html.Div(
        [
        html.Img(
            src='assets/shed_enterprises.png', 
            width='100%',
            ), 
        ],
        id="logo"
    ), 
    width=True,
    id="top_bar"
)
