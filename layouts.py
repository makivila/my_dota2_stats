from dash import html, dcc

from data import stats_kda, stats_side, stats_by_duration
from my_figure import fig


general_layout = html.Div(
    [
        html.H1(
            children="Статистика игрока Saphira the Fire в Dota 2",
            style={"textAlign": "center"},
        ),
        dcc.Graph(figure=fig),
        dcc.Dropdown(
            stats_kda.localized_name.unique(), "Lich", id="dropdown-selection"
        ),
        dcc.Graph(id="graph_kda"),
        dcc.Dropdown(
            stats_side.localized_name.unique(), "Lich", id="dropdown-selection1"
        ),
        dcc.Graph(id="graph_side"),
        dcc.Dropdown(
            stats_by_duration.localized_name.unique(), "Lich", id="dropdown-selection2"
        ),
        dcc.Graph(id="graph_category"),
    ],
    style={"margin-left": "80px", "margin-right": "80px"},
)
