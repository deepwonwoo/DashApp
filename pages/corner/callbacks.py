from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import flask
import os, io
import base64


def register_corner_callbacks(app):
    @app.callback(
        Output("tr-cards", "children"),
        [Input("upload-library", "contents")],
        [State("upload-library", "filename")],
    )
    def upload_library_button(content, filename):
        if content is not None:
            content_type, content_string = content.split(",")
            # decoded = base64.b64decode(content_string)
            print("loaed data")
            print(decoded)

            with open(decoded, "r") as f:
                print(f.readlines)
            # for line in decoded:
            #    print(line)
