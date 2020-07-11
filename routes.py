import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output, State
from flask import request

from pages.upload.layouts import upload_page
from pages.download.layouts import download_page
from pages.optimize.layouts import optimize_page
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#262B3D",
    "color": "#E2EFFA",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "12rem",
    "padding": "2rem 1rem",
}

content = html.Div(id="page-content", style=CONTENT_STYLE)


sidebar = html.Div(
    [
        # The local store will take the initial data
        # only the first time the page is loaded
        # and keep it until it is cleared.
        dcc.Store(id="user-memory", storage_type="session"),

        html.H3("AlphaSPICE"),
        html.Hr(),
        html.P("AI기반 SPICE 모델링"),
        dbc.Nav(
            [
                dbc.NavLink("1. 데이터 업로드", href="/page-1", id="page-1-link"),
                dbc.NavLink("2. 모델링 최적화", href="/page-2", id="page-2-link"),
                dbc.NavLink("3. 결과 다운로드", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


app_layout = html.Div([dcc.Location(id="url"), sidebar, content])


def register_index_callbacks(app):

    # this callback uses the current pathname to set the active state of the
    # corresponding nav link to true, allowing users to tell see page they are on

    @app.callback(
        [Output(f"page-{i}-link", "active") for i in range(1, 4)],
        [Input("url", "pathname")],
    )
    def toggle_active_links(pathname):
        if pathname == "/":
            # Treat page 1 as the homepage / index
            return True, False, False
        return [pathname == f"/page-{i}" for i in range(1, 4)]

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname in ["/", "/page-1"]:
            return upload_page()
        elif pathname == "/page-2":
            return optimize_page()
        elif pathname == "/page-3":
            return download_page()
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )
