import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import flask
import os


def register_download_callbacks(app):

    @app.callback(
        Output("corner-output", "value"),
        [Input("fit-button", "n_clicks")],
        [
            State("target-tt-vth", "value"),
            State("target-ss-vth", "value"),
            State("target-ff-vth", "value"),
        ],
    )
    def on_button_click(n, tt_vth, ss_vth, ff_vth):
        if n is None:
            corner_output = f"Corner Modeling"
        else:
            with open("./assets/templates/sp_corner", mode="r") as f:
                corner_template = f.read()
            corner_output = corner_template.replace('$dVTO_FF', f'{ff_vth}')

        return corner_output

    @app.callback(
        Output("library-text", "value"),
        [Input("library-bnt", "n_clicks")],
        [State("corner-output", "value"), State("buffer-textarea", "value")],
    )
    def make_library(n, corner_text, buffer_text):

        library_text = corner_text + "\n" + buffer_text

        return library_text

    @app.callback(
        Output("download-area", "children"),
        [Input("save-btn", "n_clicks")],
        [State("library-text", "value")],
    )
    def download_library(n, lib_text):
        if n is None:
            raise PreventUpdate

        relative_filename = os.path.join("workspace", "AI.lib")
        absolute_filename = os.path.join(os.getcwd(), relative_filename)

        with open(relative_filename, "w") as f:
            f.write(lib_text)
        uri = relative_filename
        return html.Form(
            action=uri,
            method="get",
            children=[
                html.Button(children=[
                            dbc.Button("Success", color="success", className="mr-1")], type="submit", style={"borderStyle": "none"})
            ],
        )

    @app.server.route("/workspace/<path:path>")
    def serve_static(path):
        root_dir = os.getcwd()
        return flask.send_from_directory(os.path.join(root_dir, "workspace"), path)
