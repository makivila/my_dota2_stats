from dash import html, dcc
import dash_bootstrap_components as dbc
from data import stats_kda, stats_by_duration, stats_side, winrate_by_hero
from static_plots import (
    percent_matches_by_hero,
    indicator_winrate,
    indicator_kda,
    fig_kills_assists_deaths,
)


general_layout = (
    html.Div(
        style={
            "padding": "15px",
        },
        children=[
            html.H1(
                children="Статистика игрока Saphira the Fire в Dota 2",
                style={"textAlign": "center"},
            ),
            html.Div(
                className="container_wrapper",
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.H2("Saphira the Fire", className="display-3"),
                                    html.Hr(className="my-2"),
                                    html.P(
                                        "Более подробную статистику можно посмотреть на сайте dotabuff"
                                    ),
                                    dbc.Button(
                                        "Перейти на сайт",
                                        color="secondary",
                                        outline=True,
                                        href="https://ru.dotabuff.com/players/1253662502",
                                    ),
                                ],
                                className="h-20 p-5 bg-light text-dark border rounded-3",
                            ),
                            html.Div(
                                className="container_wrapper mt-3",
                                children=[
                                    dbc.Button(
                                        "Indicators",
                                        id="indicator_button",
                                        color="primary",
                                        n_clicks=0,
                                    ),
                                    dbc.Button(
                                        "Graph by kills assists and deaths",
                                        id="kills_assists_deaths_button",
                                        color="primary",
                                        n_clicks=0,
                                    ),
                                ],
                            ),
                            html.Div(
                                className="container_wrapper mt-3",
                                children=[
                                    html.Div(
                                        [
                                            html.Div(
                                                dbc.Collapse(
                                                    dbc.Card(
                                                        dbc.CardBody(
                                                            html.Div(
                                                                children=[
                                                                    dcc.Graph(
                                                                        figure=indicator_winrate,
                                                                    ),
                                                                    dcc.Graph(
                                                                        figure=indicator_kda,
                                                                    ),
                                                                ],
                                                            ),
                                                        ),
                                                    ),
                                                    id="indicators",
                                                    is_open=False,
                                                    dimension="width",
                                                ),
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                dbc.Collapse(
                                                    dbc.Card(
                                                        dbc.CardBody(
                                                            html.Div(
                                                                [
                                                                    dcc.Graph(
                                                                        figure=fig_kills_assists_deaths
                                                                    ),
                                                                ],
                                                            ),
                                                        ),
                                                    ),
                                                    id="kills_assists_deaths_graph",
                                                    is_open=False,
                                                    dimension="width",
                                                ),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ]
                    ),
                    dcc.Graph(
                        className="mx-3",
                        figure=percent_matches_by_hero,
                        style={"height": "432px", "border": "1px solid gray"},
                    ),
                    dbc.Card(
                        [
                            dbc.CardImg(id="change_photo_hero", top=True),
                            dbc.CardBody(
                                [
                                    html.H4("Hero", className="card-title"),
                                    dcc.Dropdown(
                                        winrate_by_hero.localized_name.unique(),
                                        "Lich",
                                        id="dds_for_winrate_by_hero",
                                    ),
                                    dcc.Graph(
                                        id="indicator_winrate_by_hero",
                                    ),
                                ],
                            ),
                        ],
                        style={
                            "width": "400px",
                            "height": "580px",
                        },
                    ),
                ],
            ),
            html.Hr(style={"border-width": "6px"}),
        ],
    ),
    html.Div(
        children=[
            html.Div(),
            html.Div(
                [
                    dcc.Dropdown(
                        stats_kda.localized_name.unique(),
                        "Lich",
                        id="dropdown-selection",
                    ),
                    dcc.Graph(id="graph_kda"),
                    dcc.Dropdown(
                        stats_side.localized_name.unique(),
                        "Lich",
                        id="dropdown-selection1",
                    ),
                    dcc.Graph(id="graph_side"),
                    dcc.Dropdown(
                        stats_by_duration.localized_name.unique(),
                        "Lich",
                        id="dropdown-selection2",
                    ),
                    dcc.Graph(id="graph_category"),
                ],
                style={
                    "margin-left": "40px",
                    "margin-right": "40px",
                },
            ),
        ],
    ),
)
