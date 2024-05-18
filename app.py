from dash import dash
import dash_bootstrap_components as dbc
from layouts import general_layout


app = dash.Dash(
    __name__, title="Musina Dashboard", external_stylesheets=[dbc.themes.LITERA]
)
app.config.suppress_callback_exceptions = True
app.layout = general_layout
