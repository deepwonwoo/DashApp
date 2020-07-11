import dash
import dash_auth
from routes import app_layout, register_index_callbacks
from pages.upload.callbacks import register_upload_callbacks
from pages.optimize.callbacks import register_optimize_callbacks
from pages.download.callbacks import register_download_callbacks

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'test': 'test'
}

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=["assets/bootstrap.min.css"])


auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


app.layout = app_layout

register_index_callbacks(app)
register_upload_callbacks(app)
register_download_callbacks(app)
register_optimize_callbacks(app)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
