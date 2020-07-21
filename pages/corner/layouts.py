import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


def corner_page():

    page = html.Div(
        [
            dbc.Row(
                dbc.Col([dcc.Upload(dbc.Button("Upload File"), id="upload-library")])
            ),
            html.Hr(),
            dbc.Row([dbc.Col([html.Div(id="tr-cards")])]),
        ]
    )

    return page
