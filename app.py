from dash import dash

# import dash_core_components as dcc
import dash_bootstrap_components as dbc
from layouts import general_layout

import plotly.express as px


app = dash.Dash(
    __name__, title="Musina Dashboard", external_stylesheets=[dbc.themes.LITERA]
)
app.config.suppress_callback_exceptions = True

app.layout = general_layout
