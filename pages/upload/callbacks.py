import io
import os
import json
import pickle
import base64
import subprocess
import numpy as np
import pandas as pd
import plotly.graph_objs as go

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import request


class Measurement:
    def __init__(self):
        self.df_transfer = None
        self.transfer_vds_list = None
        self.x_Vgs = None
        self.transfer_validIndex = None
        self.df_output = None
        self.output_vgs_list = None
        self.x_Vds = None
        self.df_para = pd.read_csv("./assets/para_config.csv")
        self.output_validIndex = None


def load_measurement(contents, filename, meas, IS_TRANSFER):
    try:
        _, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)

        fig = go.Figure()
        fig.update_layout(title=filename, template="plotly_white")
        if IS_TRANSFER:
            meas.df_transfer = pd.read_excel(io.BytesIO(decoded)).fillna(0)
            meas.transfer_vds_list = meas.df_transfer.columns[1:]
            meas.x_Vgs = meas.df_transfer[meas.df_transfer.columns[0]]
            meas.transfer_validIndex = (
                meas.df_transfer[meas.transfer_vds_list]
                .ne(0)
                .apply(
                    lambda x: pd.Series(
                        [x[x].index[0] + 1, x[x].index[-1] + 1],
                        index=["StartIndex", "EndIndex"],
                    )
                )
            )

            for i, c in enumerate(meas.transfer_vds_list):
                fig.add_trace(
                    go.Scatter(
                        x=meas.x_Vgs,
                        y=np.log(meas.df_transfer[c]),
                        mode="markers",
                        marker_size=2,
                        marker_color="midnightblue",
                        name=f"vds={c}",
                    )
                )
            fig.update_xaxes(title_text="Vgs(V)")
            fig.update_yaxes(title_text="Ids(A) @ log scale")

        else:
            meas.df_output = pd.read_excel(io.BytesIO(decoded)).fillna(0)
            meas.output_vgs_list = meas.df_output.columns[1:]
            meas.x_Vds = meas.df_output[meas.df_output.columns[0]]
            meas.output_validIndex = (
                meas.df_output[meas.output_vgs_list]
                .ne(0)
                .apply(
                    lambda x: pd.Series(
                        [x[x].index[0] + 1, x[x].index[-1] + 1],
                        index=["StartIndex", "EndIndex"],
                    )
                )
            )

            for i, c in enumerate(meas.output_vgs_list):
                fig.add_trace(
                    go.Scatter(
                        x=meas.x_Vds,
                        y=meas.df_output[c],
                        mode="markers",
                        marker_size=2,
                        marker_color="midnightblue",
                        name=f"vgs={c}",
                    )
                )

            fig.update_xaxes(title_text="Vgs(V)")
            fig.update_yaxes(title_text="Ids(A)")
        result = [dcc.Graph(figure=fig)]
    except Exception as e:
        print(e)

        result = [
            dbc.Toast(
                [html.P("지원하지 않는 포맷입니다", className="mb-0")],
                id="auto-toast",
                header="포맷 에러",
                icon="primary",
                duration=4000,
            ),
        ]
        pass

    return result


def create_job(meas, username, id, tft_name, width, length, tnom, vto, mu0, tox, epsi, cgdo, cgso):

    print(username, id)

    if 0 > int(tnom):
        temp = f"Dm{tnom*-1}"
    else:
        temp = f"D{tnom:03}"

    with open("./assets/templates/sp_lib", "r") as f:
        lib_lines = f.readlines()
        with open(f"./workspace/{username}/{id}/spice.lib", "w") as f:
            for line in lib_lines:
                line = (
                    line.replace("INPUT_VTO", f"{vto}")
                    .replace("INPUT_MU0", f"{mu0}")
                    .replace("INPUT_TOX", f"{tox}")
                    .replace("INPUT_TNOM", f"{tnom}")
                    .replace("INPUT_EPSI", f"{epsi}")
                    .replace("INPUT_CGDO", f"{cgdo}")
                    .replace("INPUT_CGSO", f"{cgso}")
                    .replace("$TR_NAME", f"{tft_name}")
                    .replace("$TEMP", f"{temp}")
                )
                f.write(line)

    with open("./assets/templates/sp_in", "r") as f:
        infile_lines = f.readlines()
        with open(f"./workspace/{username}/{id}/base_transfer.in", "w") as f:
            for line in infile_lines:
                if line.startswith("$SETTINGS"):
                    line = f".dc vgs {np.min(meas.x_Vgs)} {np.max(meas.x_Vgs)} {np.subtract(meas.x_Vgs[1]*100, meas.x_Vgs[0]*100)/100}\n"
                    line += ".param vds = 10\n"
                    line += ".param vgs = 0\n"
                    line += f"m1 net g s {tft_name}, W={width}u L={length}u\n"
                elif line.startswith("$LIB"):
                    line = f".lib './workspace/{username}/{id}/spice.lib' TT\n"
                    line = f".lib './workspace/{username}/{id}/spice.lib' {temp}\n"
                elif line.startswith("$ALTERS"):
                    line = "\n"
                    for v in meas.transfer_vds_list:
                        line += f".ALTER\n"
                        line += f".PARAM vds = {v}\n\n"
                f.write(line)

    with open("./assets/templates/sp_in", "r") as f:
        infile_lines = f.readlines()
        with open(f"./workspace/{username}/{id}/base_output.in", "w") as f:
            for line in infile_lines:
                if line.startswith("$SETTINGS"):
                    line = f".dc vds {np.min(meas.x_Vds)} {np.max(meas.x_Vds)} {np.subtract(meas.x_Vds[1]*100, meas.x_Vds[0]*100)/100}\n"
                    line += ".param vgs = 10\n"
                    line += ".param vds = 0\n"
                    line += f"m1 net g s {tft_name}, W={width}u L={length}u\n"
                elif line.startswith("$LIB"):
                    line = f".lib './workspace/{username}/{id}/spice.lib' TT\n"
                    line = f".lib './workspace/{username}/{id}/spice.lib' {temp}\n"
                elif line.startswith("$ALTERS"):
                    line = "\n"
                    for v in meas.output_vgs_list:
                        line += f".ALTER\n"
                        line += f".PARAM vgs = {v}\n\n"
                f.write(line)

    with open(f"./workspace/{username}/{id}/meas.pickle", "wb") as f:
        pickle.dump(meas, f)

    my_env = os.environ.copy()

    log = open(f"./workspace/{username}/{id}/log.txt", "wb")

    proc = subprocess.Popen(

        f"python ./utils/rl.py --id {id} --username {username}",
        stdout=log,
        stderr=log,
        shell=True,
        # preexec_fn=os.setsid,
        # env=my_env,
    )

    try:
        with open(f"./workspace/{username}/modeling.json", "r") as json_file:
            json_data = json.load(json_file)
    except IOError:
        json_data = {}
        json_data["modeling"] = []

    json_data["modeling"].append(
        {
            "job_id": id,
            "tft_name": tft_name,
            "width": width,
            "length": length,
            "temperature": temp,
            "vto": vto,
            "mu0": mu0,
            "pid": proc.pid,
            "running": True,
            "selected": False,
        }
    )
    with open(f"./workspace/{username}/modeling.json", "w") as outfile:
        json.dump(json_data, outfile, indent=4)


meas = Measurement()


def register_upload_callbacks(app):

    @app.callback(
        Output(f"vis-transfer-meas", "children"),
        [Input(f"upload-transfer-meas", "contents")],
        [State(f"upload-transfer-meas", "filename")],
    )
    def upload_transfer_meas(contents, filename):
        if contents is not None:
            return load_measurement(contents, filename, meas, True)

    @app.callback(
        Output(f"vis-output-meas", "children"),
        [Input(f"upload-output-meas", "contents")],
        [State(f"upload-output-meas", "filename")],
    )
    def upload_output_meas(contents, filename):
        if contents is not None:
            return load_measurement(contents, filename, meas, False)

    @app.callback(
        [
            Output("modeling-toast", "is_open"),
            Output("modeling-toast", "header"),
            Output("modeling-toast", "children"),
            Output("modeling-toast", "icon")
        ],
        [Input("create-modeling-btn", "n_clicks")],
        [
            State(f"tft-name-input", "value"),
            State(f"tft-width-input", "value"),
            State(f"tft-length-input", "value"),
            State(f"temperature-input", "value"),
            State(f"vto-input", "value"),
            State(f"mu0-input", "value"),
            State(f"tox-input", "value"),
            State(f"epsi-input", "value"),
            State(f"cgdo-input", "value"),
            State(f"cgso-input", "value"),
        ],
    )
    def activate_model_card(
        n, tft_name, width, length, tnom, vto, mu0, tox, epsi, cgdo, cgso
    ):
        username = request.authorization['username']
        if n is None:
            raise PreventUpdate

        try:
            with open(f"./workspace/{username}/modeling.json", "r") as json_file:
                json_data = json.load(json_file)
        except IOError:
            json_data = {}
            json_data["modeling"] = []
            json_data["library"] = []

        for id in range(1, 3 + 1):
            if not os.path.exists(f"./workspace/{username}/{id}"):
                os.makedirs(f"./workspace/{username}/{id}")

                create_job(meas, username, id, tft_name, width,
                           length, tnom, vto, mu0, tox, epsi, cgdo, cgso)

                return (
                    True,
                    "Modeling Starts",
                    f"TR. info: {tft_name}({width}u/{length}u)@{tnom}\u2103",
                    "info",
                )

        return (True, "Too many Modelings!", f"modeling over 3 cases", "danger")
