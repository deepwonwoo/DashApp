import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


def corner_modeling():

    with open("./assets/templates/sp_lib", mode="r") as f:
        buffer_lib = f.read()

    return html.Div(
        [
            html.H5("Selected Modeling"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Textarea(
                            id="buffer-textarea",
                            value=buffer_lib,
                            style={"width": "100%", "height": 500},
                        )
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Label("VTH"), width=1),
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon(
                                        "TT", addon_type="prepend"),
                                    dbc.Input(id="target-tt-vth", value=0.27),
                                ],
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon(
                                        "SS", addon_type="prepend"),
                                    dbc.Input(id="target-ss-vth"),
                                ],
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon(
                                        "FF", addon_type="prepend"),
                                    dbc.Input(id="target-ff-vth"),
                                ],
                            ),
                        ]
                    ),
                    dbc.Col(dbc.Label("Ion"), width=1),
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon(
                                        "TT", addon_type="prepend"),
                                    dbc.Input(id="target-tt-ion", value=8.36),
                                ],
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon(
                                        "SS", addon_type="prepend"),
                                    dbc.Input(id="target-ss-ion"),
                                ],
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon(
                                        "FF", addon_type="prepend"),
                                    dbc.Input(id="target-ff-ion"),
                                ],
                            ),
                        ]
                    ),
                    dbc.Col(
                        [dbc.Button("Fit Corner", id="fit-button",
                                    className="mr-2"), ]
                    ),
                ],
                className="m-1",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Textarea(
                                id="corner-output",
                                value="library",
                                style={"width": "100%", "height": 100},
                                loading_state={'is_loading': True}
                            ),
                        ]
                    ),
                ]
            ),
            dbc.Button(
                "Apply to Library", color="primary", id="library-bnt", block=True
            )
        ]
    )


def library_output():

    return html.Div(
        [
            html.H5("Modeling Library"),
            dcc.Textarea(
                id="library-text",
                value="",
                style={"width": "100%", "height": 730},
            ),
            dbc.Row(
                [
                    dbc.Button(
                        "Save Library",
                        id="save-btn",
                        color="info",
                        className="mr-1",
                    ),
                    html.Div("", id="download-area")
                ], className='ml-2'
            )
        ],
    )


def download_page():

    page = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(corner_modeling(), width=6),
                    dbc.Col(library_output(), width=6),
                ]
            ),
        ]
    )

    return page
