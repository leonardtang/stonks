import dash_bootstrap_components as dbc


def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Stocks", href="/stocks")),
            dbc.NavItem(dbc.NavLink("Crypto", href="/crypto")),
            dbc.NavItem(dbc.NavLink("Volatility", href="/volatility")),
            dbc.NavItem(dbc.NavLink("Pulse Check", href="/sentiment"))
        ],
        brand="Stonks: A Leonard Tang Production",
        brand_href="https://leonardtang.me",
        sticky="top",
        fluid=True
    )
    return navbar
