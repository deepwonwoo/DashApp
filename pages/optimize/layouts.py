import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from flask import request
import json


def create_card(model, username):
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Row(
                    [
                        dbc.Col(
                            [f"No.{model['job_id']})  {model['tft_name']}"]),
                        dbc.Col(
                            [
                                dbc.Button(
                                    "X",
                                    id=f"kill-{username}-{model['job_id']}",
                                    color="secondary",
                                    style={
                                        "right": "5px",
                                        "padding": "1px 5px",
                                        "position": "absolute",
                                    },
                                )
                            ],
                        ),
                    ]
                )
            ),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.P(
                                        [
                                            f"L/W = {model['width']}u / {model['length']}u"
                                        ]
                                    ),
                                    html.P(
                                        [f"Temperature = {model['temperature']}"]),
                                    html.P(
                                        [f"VTO = {model['vto']},  MU0 = {model['mu0']}"]
                                    ),
                                ],
                                width=3,
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        id=f'logtable-{model["job_id"]}'),
                                    html.Div(
                                        id=f'plot-{model["job_id"]}',),
                                ],
                                width=9,
                            ),
                        ]
                    )
                ]
            ),
        ],
        id=f"jobcard-{username}-{model['job_id']}",
        outline=True,
        className="mt-2",
    )


def optimize_page():
    username = request.authorization['username']
    try:
        with open(f"./workspace/{username}/modeling.json", "r") as json_file:
            json_data = json.load(json_file)
    except IOError:
        json_data = {}
        json_data["modeling"] = []
        json_data["library"] = []

    cards = []
    for m in json_data["modeling"]:
        cards.append(create_card(m, username))

    return html.Div(
        [
            dcc.Interval(
                id=f"interval-train",
                interval=1 * 10000,  # in milliseconds
                n_intervals=0,
            ),
            html.Div(cards),
        ]
    )
