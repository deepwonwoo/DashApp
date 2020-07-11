import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import os

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from flask import request
from si_prefix import si_format
import pandas as pd
import dash_table


def update_logtable(username, id):

    try:

        df = pd.read_csv(f"workspace/{username}/{id}/trained_para.log")
        df.drop("episode", axis=1, inplace=True)
        df.drop("step", axis=1, inplace=True)

        for c in df.columns:
            df[c] = df[c].apply(si_format)

        if "error" in df.columns:
            d = df.sort_values(by="error", ascending=True)[
                :3].to_dict("records")
        else:
            d = df.to_dict("records")

        datatable = dash_table.DataTable(
            id=f"check-data-{id}",
            columns=[{"name": c, "id": c} for c in df.columns],
            data=d,
            row_selectable="single",
            style_cell={
                "height": "auto",
                "minWidth": "0px",
                "maxWidth": "100px",
                "whiteSpace": "normal",
            },
        )
    except IOError:
        datatable = None

    return datatable


def register_optimize_callbacks(app):
    # . live Updating log data table
    @app.callback(
        [Output(f"logtable-{i+1}", "children") for i in range(2)],
        [Input(f"interval-train", "n_intervals")],
    )
    def update_history_log(n):
        username = request.authorization['username']
        return [update_logtable(username, i + 1) for i in range(2)]
