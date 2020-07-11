import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
from flask import request


tft_info_input = html.Div(
    [
        dbc.FormGroup(
            [
                dbc.Label("TFT name:", className="ml-3"),
                dbc.Col(
                    dbc.Input(type="text", id="tft-name-input",
                              placeholder="Type TFT name"),
                ),
            ],
            row=True,
        ),
        dbc.FormGroup(
            [
                dbc.Label("Width/Length:", className="ml-3"),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.Input(
                                id=f"tft-width-input", placeholder="Width", type="number"
                            ),
                            dbc.InputGroupAddon("\u03BC", addon_type="append"),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.Input(
                                id=f"tft-length-input", placeholder="Length", type="number"
                            ),
                            dbc.InputGroupAddon("\u03BC", addon_type="append"),
                        ]
                    )
                ),
            ],
            row=True,
        )
    ]
)

temperature_input = dbc.FormGroup(
    [
        dbc.Label("Temperature", className="ml-3"),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.Input(
                        id="temperature-input", type="number", min=-30, max=100, step=1
                    ),
                    dbc.InputGroupAddon("\u2103", addon_type="append"),
                ],
                className="mb-3",
            ),
            width=3,
        ),
    ],
    row=True,
)

fixed_parameter_input = dbc.Row(
    [
        dbc.Label("Fixed Parameters:"),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("VTO", addon_type="prepend"),
                    dbc.Input(type="number", id="vto-input"),
                ]
            )
        ),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("MU0", addon_type="prepend"),
                    dbc.Input(type="number", id="mu0-input"),
                ]
            )
        ),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("TOX", addon_type="prepend"),
                    dbc.Input(type="number", id="tox-input", value="1.5e-07"),
                ]
            )
        ),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("EPSI", addon_type="prepend"),
                    dbc.Input(type="number", id="epsi-input", value="3.89"),
                ]
            )
        ),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("CGDO", addon_type="prepend"),
                    dbc.Input(type="number", id="cgdo-input",
                              value="7.42853e-11"),
                ]
            )
        ),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("CGSO", addon_type="prepend"),
                    dbc.Input(type="number", id="cgso-input",
                              value="7.42853e-11"),
                ]
            )
        ),
    ], className="ml-0"
)


modeling_inputs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([tft_info_input]),
                dbc.Col([temperature_input]),
            ]
        ),
        fixed_parameter_input

    ]
)


fixed_parameter_input = dbc.Row(
    [
        dbc.Label("Fixed Parameters:", className="ml-3"),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("VTO", addon_type="prepend"),
                    dbc.Input(type="number", id="vto-input"),
                ]
            )
        ),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("MU0", addon_type="prepend"),
                    dbc.Input(type="number", id="mu0-input"),
                ]
            )
        ),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("TOX", addon_type="prepend"),
                    dbc.Input(type="number", id="tox-input", value="1.5e-07"),
                ]
            )
        ),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("EPSI", addon_type="prepend"),
                    dbc.Input(type="number", id="epsi-input", value="3.89"),
                ]
            )
        ),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("CGDO", addon_type="prepend"),
                    dbc.Input(type="number", id="cgdo-input",
                              value="7.42853e-11"),
                ]
            )
        ),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("CGSO", addon_type="prepend"),
                    dbc.Input(type="number", id="cgso-input",
                              value="7.42853e-11"),
                ]
            )
        ),
    ]
)

tuning_parameter_input = dbc.Row(
    [
        dbc.Label("Tuning Parameters:", className="ml-3"),
        dbc.Col(
            dcc.Dropdown(
                options=[{"label": p, "value": p} for p in df_para.iloc[:, 0]],
                multi=True,
                value=[p for p in df_para.iloc[:, 0]],
            ),
            width=8,
        ),
    ],
    className="mt-3",
)

tuning_para_table = dbc.Row(
    [
        dbc.Col(
            dash_table.DataTable(
                columns=[
                    {"name": c, "id": f"step{s+1}-{c}"} for c in df_para.columns[0:3]
                ],
                data=[
                    {
                        f"step{s+1}-Parameters": row[0],
                        f"step{s+1}-Min": to_si(row[1]),
                        f"step{s+1}-Max": to_si(row[2]),
                    }
                    for i, row in df_para.iterrows()
                    if row[3] == s + 1
                ],
                editable=True,
                style_cell={"minWidth": 45, "maxWidth": 45, "width": 45},
                style_data_conditional=[
                    {
                        "if": {"column_id": f"step{s+1}-Parameters", },
                        "color": "black",
                        "fontWeight": "bold",
                        "backgroundColor": color,
                        "backgroundOpacity": 0.5,
                    }
                ],
            ),
            className="m-3",
        )
        for s, color in enumerate(["#fe9a9a", "#b8ecfe", "#aefec2", "#fef8ae"])
    ]
)

measurement_upload = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Transfer Curve", className="card-title"),
                        dcc.Upload(
                            id=f"upload-transfer-meas",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select Files")]
                            ),
                            style={
                                "width": "100%",
                                "height": "35px",
                                "lineHeight": "35px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "5px",
                            },
                        ),
                        html.Div(id=f"vis-transfer-meas"),
                    ]
                ),
                color="light",
                outline=True,
            )
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Output Curve", className="card-title"),
                        dcc.Upload(
                            id=f"upload-output-meas",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select Files")]
                            ),
                            style={
                                "width": "100%",
                                "height": "35px",
                                "lineHeight": "35px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "5px",
                            },
                        ),
                        html.Div(id=f"vis-output-meas"),
                    ]
                ),
                color="light",
                outline=True,
            )
        ),
    ]
)


def upload_page():
    username = request.authorization['username']

    page = dbc.Card(
        [
            dbc.CardHeader(f"{username}님, 어서오세요!"),
            dbc.CardBody(
                [
                    html.H5("모델링 카드 생성", className="card-title"),
                    html.P("모델링 정보를 입력해 주세요."),
                    html.Hr(),
                    modeling_inputs,
                    tuning_para_table,
                    measurement_upload
                ]
            )
        ]
    )

    return page
